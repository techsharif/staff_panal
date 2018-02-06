import re

from django import template
from django.urls import reverse


class _Menu:
    parents = []
    childs = []
    models_icon = {}

    def clear(self):
        self.parents = []
        self.childs = []

    def add(self, label, link='', icon='', id='', parent=''):

        if id == '':
            id = label

        if parent != '':
            child = {
                id: {
                    'label': label,
                    'link': link,
                    'icon': icon,
                    'childs': []
                }
            }

            self.childs.append(child)

            for idx, parent_item in enumerate(self.parents):

                if parent in parent_item:
                    self.parents[idx][parent]['childs'].append(child)
                else:
                    for idx, child_item in enumerate(self.childs):
                        if parent in child_item:
                            self.childs[idx][parent]['childs'].append(child)

        else:
            self.parents.append({
                id: {
                    'label': label,
                    'link': link,
                    'icon': icon,
                    'childs': []
                }
            })

    def render(self, context, menus={}):
        r = ''

        if len(menus) <= 0:
            # sorted(self.parents)
            menus = self.parents

            r = '<li><a href="' + reverse('admin:index') + '">Home</a></li>'

        for group in menus:
            key = [key for key in group][0]
            # icon = '<i class="fa fa-circle"></i>'
            css_class_name = group[key]['label'].replace(' ', '')

            # if group[key]['icon'] != '':
            #     if re.match(r'\<([a-z]*)\b[^\>]*\>(.*?)\<\/\1\>', group[key]['icon']):
            #         icon = group[key]['icon']
            #     else:
            #         icon = '<i class="%s"></i>' % (group[key]['icon'])
            # todo need to add icon on HOme and the next one

            if len(group[key]['childs']) > 0:
                r += '<li><a data-toggle="collapse" href="#nav-%s">%s<i ' \
                     'class="fa fa-angle-left pull-right"></i></a><div class="collapse" id="nav-%s"><ul ' \
                     'class="nav">\n' % (
                         css_class_name, group[key]['label'], css_class_name)

                r += self.render(context, group[key]['childs'])

                r += '</ul></div></li>\n'

            else:
                r += '<li><a href="%s">%s</a></li>\n' % (
                    group[key]['link'], group[key]['label'])

        return r

    def admin_apps(self, context, r):
        current_url = context['request'].path

        for app in context['available_apps']:

            css_class_name = app['name'].replace(' ', '')

            # TODO need to add menu after <a> on follwoing two
            if app['app_url'] in current_url:
                r += '<li class="active"><a data-toggle="collapse" href="#nav-%s">%s <b ' \
                     'class="caret"></b></a><div class="collapse" id="nav-%s"><ul class="nav">\n' % (
                         css_class_name, app['name'], css_class_name)
            else:
                r += '<li><a data-toggle="collapse" href="#nav-%s">%s <b ' \
                     'class="caret"></b></a><div class="collapse" id="nav-%s"><ul class="nav">\n' % (
                         css_class_name, app['name'], css_class_name)

            for model in app['models']:
                if 'add_url' in model:
                    url = model['add_url']

                if 'change_url' in model:
                    url = model['change_url']

                # if 'delete_url' in model:
                #     url = model['delete_url']

                if 'admin_url' in model:
                    url = model['admin_url']

                # TODO: adjust the design for menu icon
                # icon = '<i class="fa fa-circle-o"></i>'
                # if model['object_name'].title() in self.models_icon:
                #     if self.models_icon[model['object_name'].title()] != '':
                #         if re.match(r'\<([a-z]*)\b[^\>]*\>(.*?)\<\/\1\>',
                #                     self.models_icon[model['object_name'].title()]):
                #             icon = self.models_icon[model['object_name'].title()]
                #         else:
                #             icon = '<i class="%s"></i>' % (self.models_icon[model['object_name'].title()])

                if model['admin_url'] in current_url:
                    r += '<li class="active"><a href="%s">%s</a></li>' % (url, model['name'])
                else:
                    r += '<li><a href="%s"> %s</a></li>' % (url, model['name'])

            r += '</ul></li>\n'

        return r

    def set_model_icon(self, model_name, icon):
        self.models_icon[model_name.title()] = icon

    def get_model_icon(self, context):

        icon = '<i class="fa fa-circle-o"></i>'
        if context['model']['object_name'].title() in self.models_icon:

            if self.models_icon[context['model']['object_name'].title()] != '':
                if re.match(r'\<([a-z]*)\b[^\>]*\>(.*?)\<\/\1\>',
                            self.models_icon[context['model']['object_name'].title()]):
                    icon = self.models_icon[context['model']['object_name']]
                else:
                    icon = '<i class="%s"></i>' % (self.models_icon[context['model']['object_name'].title()])

        return icon


register = template.Library()

Menu = _Menu()


@register.simple_tag(takes_context=True)
def menu(context):
    # user = context['request'].user

    return Menu.admin_apps(context, Menu.render(context))


@register.simple_tag(takes_context=True)
def icon(context):
    return Menu.get_model_icon(context)
