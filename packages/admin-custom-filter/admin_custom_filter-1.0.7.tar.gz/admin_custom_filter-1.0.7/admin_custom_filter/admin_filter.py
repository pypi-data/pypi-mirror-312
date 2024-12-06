from django.contrib.admin import ModelAdmin
import re
import json
from django.core.exceptions import FieldError, FieldDoesNotExist
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe
from bleach import clean as xss_clean
from .models import CustomAdminFilter

def get_field(model, field_name):
    try:
        return model._meta.get_field(field_name)
    except FieldDoesNotExist:
        return None

def create_dynamic_field_link_function(field):
    field_name = field.replace("_set", "") if "_set" in field else field
    func = field_name
    def get_field_link(instance):
        foreign_key_instance = getattr(instance, field)
        if foreign_key_instance:
            try:
                url = reverse(f"admin:{instance._meta.get_field(field_name).related_model._meta.app_label}_{field}_change", args=[foreign_key_instance.pk])
            except Exception as e:
                try:
                    url = reverse(f"admin:{instance._meta.get_field(field_name).related_model._meta.app_label}_{instance._meta.get_field(field_name).related_model._meta.model_name}_change", args=[foreign_key_instance.pk])
                except NoReverseMatch as e:
                    return None
            link = '<a href="%s">%s</a>' % (url, xss_clean(str(foreign_key_instance), strip=True))
            return mark_safe(link)
        return None
    get_field_link.short_description = field_name
    globals()[func] = get_field_link
    return globals()[func]

def create_dynamic_many_relation_link_function(field):
    field_name = field.replace("_set", "") if "_set" in field else field
    func = field_name
    def get_many_field_link(instance):
        try:
            url = reverse(f"admin:{instance._meta.get_field(field_name).related_model._meta.app_label}_{field_name}_changelist")
        except Exception as e:
            try:
                url = reverse(f"admin:{instance._meta.get_field(field_name).related_model._meta.app_label}_{instance._meta.get_field(field_name).related_model._meta.model_name}_changelist")
            except NoReverseMatch as e:
                return None
        query_param = instance._meta.verbose_name.replace(" ", "_").lower() if hasattr(instance._meta, "verbose_name_plural") and instance._meta.verbose_name else instance._meta.model_name
        fetched_field = get_field(instance._meta.model, field_name)
        # if fetched_field and fetched_field.is_relation and fetched_field.many_to_many:
        #     query_param = query_param + "s"
        link = '<a href="%s?%s">%s</a>' % (url, f"{query_param}__{fetched_field.model._meta.pk.column}__exact={instance.pk}", xss_clean(f"{instance} {field_name}s", strip=True))
        return mark_safe(link)
    get_many_field_link.short_description = field_name
    globals()[func] = get_many_field_link
    return globals()[func]

class AdminCustomFilter(ModelAdmin):
    # change_list_template = "/admin_custom_filter/templates/admin/change_list.html"
    filter = None
    default_list_filter = []
    default_list_display = []
    default_search_fields = []
    default_date_hierarchy = None
    default_ordering = None
    default_list_per_page = 50
    list_filter = []
    list_display = []
    search_fields = []
    ordering = None
    filters_by_selected = []
    searches_by_selected = []
    list_displays_selected = []
    link_fields_selected = []
    list_per_page = 50

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_list_filter = self.list_filter
        self.default_search_fields = self.search_fields
        self.default_list_display = self.list_display
        self.default_date_hierarchy = self.date_hierarchy
        self.default_ordering = self.ordering
        self.default_list_per_page  = self.list_per_page


    def changelist_view(self, request, extra_context=None):
        if request.method == "POST":
            filters_by = request.POST.getlist("filters_by")
            searches_by = request.POST.getlist("searches_by")
            list_displays = request.POST.getlist("list_displays")
            link_fields = request.POST.getlist("list_displays_link")
            date_hierarchy = request.POST.get("date_hierarchy")
            order_by = request.POST.get("order_by")
            list_per_page = request.POST.get("list_per_page")
            filter, created = CustomAdminFilter.objects.get_or_create(admin=request.user, model=self.opts.model._meta.label)
            filter.filters = json.dumps(filters_by) if len(filters_by) > 0 else None
            filter.searches = json.dumps(searches_by) if len(searches_by) > 0 else None
            filter.displays = json.dumps(list_displays + link_fields) if len(link_fields) > 0 else json.dumps(list_displays) if len(list_displays) > 0 else None
            filter.link_fields = json.dumps(link_fields) if len(link_fields) > 0 else None
            filter.date_hierarchy = date_hierarchy if date_hierarchy != "null" and get_field(self.opts.model, "created_at") else None
            filter.order_by = order_by if order_by != "null" and get_field(self.opts.model, "created_at") else None
            filter.list_per_page = int(list_per_page) if list_per_page else self.default_list_per_page
            filter.save()
            self.filter = filter
        else:
            self.filter = self.get_filter(request)
        if extra_context is None:
            extra_context = {}
        self.set_filter_fields()
        self.set_search_fields()
        self.set_list_display()
        self.set_ordering()
        self.set_list_per_page()
        self.set_date_hierarchy()
        
        display_fields = []
        for field in self.opts.model._meta.get_fields():
            if not field.is_relation:
                display_fields.append({"display_name": re.sub("([a-z])([A-Z])","\g<1> \g<2>", field.name).replace("_", " ").lower(), "field_name": field.name, "can_be_link": False, "is_many": False})
            elif field.is_relation and (field.one_to_one or field.many_to_one):
                display_fields.append({"display_name": re.sub("([a-z])([A-Z])","\g<1> \g<2>", field.name).replace("_", " ").lower(), "field_name": field.related_name if hasattr(field, "related_name") and field.related_name else field.name, "can_be_link": True, "is_many": False})
            elif field.is_relation and (field.one_to_many or field.many_to_many):
                display_fields.append({"display_name": re.sub("([a-z])([A-Z])","\g<1> \g<2>", field.name).replace("_", " ").lower(), "field_name": field.related_name if hasattr(field, "related_name") and field.related_name else f"{field.name}_set", "can_be_link": True, "is_many": True})
                
        extra_context['need_filter'] = True
        extra_context['model_fields'] = [{"display_name": re.sub("([a-z])([A-Z])","\g<1> \g<2>", field.name).replace("_", " ").lower(), "field_name": field.name, "is_hidden": True if (str(type(field)) == "<class 'django_cryptography.fields.EncryptedCharField'>") else False} for field in self.opts.model._meta.get_fields()]
        extra_context['display_fields'] = display_fields
        extra_context['filters_by_selected'] = self.filters_by_selected
        extra_context['searches_by_selected'] = self.searches_by_selected
        extra_context['list_displays_selected'] = self.list_displays_selected
        extra_context['link_fields_selected'] = self.link_fields_selected
        extra_context['date_hierarchy_selected'] = self.date_hierarchy
        extra_context['order_by_selected'] = " ".join(self.ordering) if self.ordering else None
        extra_context['list_per_page'] = self.list_per_page
        return super().changelist_view(request, extra_context)
    
    
    def get_search_results(self, request, queryset, search_term):
        try:
            return super().get_search_results(request, queryset, search_term.strip())
        except FieldError:
            search_term = search_term.strip()
            matched_search = None
            for search_field in self.search_fields:
                field = get_field(self.opts.model, search_field)
                if field and field.is_relation:
                    for foreign_key_field in field.related_model._meta.get_fields():
                        if not foreign_key_field.is_relation:
                            try:
                                filter = {
                                    f"{field.name}__{foreign_key_field.name}__icontains": f"{search_term}"
                                }
                                if queryset.filter(**filter).exists():
                                    matched_search = queryset.filter(**filter)
                                    break
                            except Exception as e:
                                continue
                    if matched_search is None:
                        search_term = search_term.split(" ")
                        matched_search = []
                        for foreign_key_field in field.related_model._meta.get_fields():
                            if not foreign_key_field.is_relation:
                                try:
                                    for term in search_term:
                                        filter = {
                                            f"{field.name}__{foreign_key_field.name}__icontains": f"{term.split()}"
                                        }
                                        if queryset.filter(**filter).exists():
                                            queries = queryset.filter(**filter)
                                            for query in queries:
                                                if query.pk not in matched_search:
                                                    matched_search.append(query.pk)
                                except Exception as e:
                                    continue
                        matched_search = queryset.filter(pk__in=matched_search)
                elif field and not field.is_relation:
                    search_term = " ".join(search_term).strip() if type(search_term) == list else search_term
                    if str(type(field)) == "<class 'django_cryptography.fields.EncryptedCharField'>":
                        matched_search = []
                        queries = queryset.filter().values("pk", search_field)
                        for query in queries:
                            if search_term.lower() in query[search_field].lower():
                                if query["pk"] not in matched_search:
                                    matched_search.append(query["pk"])
                        matched_search = queryset.filter(pk__in= matched_search)
                        if matched_search.count() == 0:
                            matched_search = []
                            search_term = search_term.split(" ")
                            for query in queries:
                                for term in search_term:
                                    if re.search(term.lower(), query[search_field].lower()):
                                        if query["pk"] not in matched_search:
                                            matched_search.append(query["pk"])
                            matched_search = queryset.filter(pk__in= matched_search)
                    else:
                        search_term = " ".join(search_term).strip() if type(search_term) == list else search_term
                        try:
                            filter = {
                                f"{field.name}__icontains": f"{search_term}",
                            }
                            if queryset.filter(**filter).exists():
                                matched_search = queryset.filter(**filter)
                                break
                        except Exception as e:
                            continue
            if matched_search is None:
                matched_search = queryset.filter(pk=0)
            return matched_search, True

    def get_filter(self, request):
        return CustomAdminFilter.objects.filter(admin=request.user, model=self.opts.model._meta.label).first()

    def set_filter_fields(self):
        self.list_filter = json.loads(self.filter.filters) if hasattr(self.filter, "filters") and self.filter.filters else self.default_list_filter
        self.filters_by_selected = json.loads(self.filter.filters) if hasattr(self.filter, "filters") and self.filter.filters else []
    
    def set_search_fields(self):
      self.search_fields = json.loads(self.filter.searches) if hasattr(self.filter, "searches") and self.filter.searches else self.default_search_fields
      self.searches_by_selected = json.loads(self.filter.searches) if hasattr(self.filter, "searches") and self.filter.searches else []
    
    def set_list_display(self):
        self.list_display = json.loads(self.filter.displays) if hasattr(self.filter, "displays") and self.filter.displays else self.default_list_display
        link_fields = json.loads(self.filter.link_fields) if hasattr(self.filter, "link_fields") and self.filter.link_fields else []
        for field in link_fields:
            if field in self.list_display:
                    field_name = field.replace("_set", "") if "_set" in field else field
                    self.list_display.remove(field)
                    self.list_display.append(create_dynamic_many_relation_link_function(field) if (self.opts.model._meta.get_field(field_name).one_to_many or self.opts.model._meta.get_field(field_name).many_to_many) else create_dynamic_field_link_function(field))
        self.list_displays_selected = json.loads(self.filter.displays) if hasattr(self.filter, "displays") and self.filter.displays else []
        self.link_fields_selected = json.loads(self.filter.link_fields) if hasattr(self.filter, "link_fields") and self.filter.link_fields else []
    
    def set_date_hierarchy(self):
        self.date_hierarchy = self.filter.date_hierarchy if hasattr(self.filter, "date_hierarchy") and self.filter.date_hierarchy else self.default_date_hierarchy
    
    def set_ordering(self):
        self.ordering = self.filter.order_by.split(" ") if hasattr(self.filter, "order_by") and self.filter.order_by else self.default_ordering
    
    def set_list_per_page(self):
        self.list_per_page = self.filter.list_per_page if hasattr(self.filter, "list_per_page") and self.filter.list_per_page else self.default_list_per_page
