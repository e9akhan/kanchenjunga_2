"""
    Module name :- views.
"""


from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q
from store.models import EquipmentType, Equipment, Allocation
from store.forms import EquipmentTypeForm, UpdatequipmentTypeForm, EquipmentForm, UpdateEquipmentForm

# Create your views here.

class Dashboard(ListView):
    """
        Dashboard
    """
    template_name = 'store/dashboard.html'
    model = EquipmentType
    context_object_name = 'equipment_types'


class CreateEquipmentType(CreateView):
    """
        Create Equipment Type
    """
    model = EquipmentType
    template_name = 'store/form.html'
    form_class = EquipmentTypeForm


    def get_success_url(self) -> str:
        """
            get_success_url
        """
        return reverse_lazy('store:dashboard')


    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Equipment Type'
        context['header'] = 'Add Equipment Type'
        return context
    

class UpdateEquipmentType(UpdateView):
    """
        Create Equipment Type
    """
    model = EquipmentType
    template_name = 'store/form.html'
    form_class = UpdatequipmentTypeForm


    def get_success_url(self) -> str:
        """
            get_success_url
        """
        return reverse_lazy('store:dashboard')


    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Equipment Type'
        context['header'] = 'Update Equipment Type'
        return context


class ListEquipment(ListView):
    """
        List Equipment
    """
    model = Equipment
    template_name = 'store/list.html'


    def get_queryset(self):
        """
            get_queryset
        """
        equipment_type = self.kwargs['equipment_type']
        query = self.model.objects.filter(equipment_type__slug__icontains = equipment_type)

        search = self.request.GET.get('search', None)

        if search:
            return query.filter(
                Q(label__icontains=search) | Q(model_number__icontains=search)
                | Q(serial_number__icontains=search) | Q(buy_date__icontains=search)
            )
        under_repair = self.request.GET.get('under_repair', None)
        if under_repair:
            return query.filter(under_repair=True)
        
        return query.filter(functional=True)


    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        context['equipments_list'] = True
        context['equipment_type'] = self.kwargs['equipment_type']
        return context


class CreateEquipment(CreateView):
    """
        Create Equipment.
    """
    model = Equipment
    form_class = EquipmentForm
    template_name = 'store/form.html'


    def get_success_url(self) -> str:
        """
            get_success_url
        """
        return reverse_lazy('store:add-equipment')


    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Equipment'
        context['header'] = 'Add Equipment'
        return context
    

class UpdateEquipment(UpdateView):
    """
        Update Equipment.
    """
    model = Equipment
    form_class = UpdateEquipmentForm
    template_name = 'store/form.html'


    def get_success_url(self):
        """
            get_context_data
        """
        return reverse_lazy('store:dashboard')


    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Equipment'
        context['header'] = 'Update Equipment'
        return context


class DeleteEquipment(DeleteView):
    """
        Delete Equipment.
    """
    model = Equipment
    template_name = 'store/form.html'


    def get_success_url(self) -> str:
        """
            get_success_url
        """
        return reverse_lazy('store:dashboard')


    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Equipment'
        context['header'] = 'Delete Equipment'
        context['headline'] = f'Do you want to delete {self.get_object()}'
        return context
    

class DetailEquipment(DetailView):
    """
        Detail Equipment
    """
    template_name = 'store/detail.html'
    model = Equipment


    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.get_object().label}'
        return context


class ListAllocation(ListView):
    """
        List Allocation
    """
    model = Allocation
    template_name = 'store/list.html'


    def get_queryset(self):
        """
            get_queryset
        """
        query = self.model.objects.filter(returned=False)
        equipment_type = self.request.GET.get('equipment_type', None)

        if equipment_type:
            return query.filter(equipment__equipment_type__slug=equipment_type)

        search = self.request.GET.get('search', None)
        
        if search:
            equipment = Allocation.objects.filter(equipment__label=search).exists()

            if equipment:
                return Allocation.objects.filter(equipment__label=search)
            else:
                return query.filter(
                    Q(user__icontains = search) |
                    Q(allocated_date__icontains = search) | 
                    Q(release_date__icontains = search)
                )
            
        return query


    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Allocations'
        context['total'] = self.get_queryset().count()
        context['equipment_types'] = [('', 'All')] + [(eqp.slug, eqp.name) for eqp in EquipmentType.objects.all()]
        return context
    

class CreateAllocation(CreateView):
    """
        Create Allocation
    """
    model = Allocation
    template_name = 'store/form.html'
    

    def get_success_url(self) -> str:
        return reverse_lazy('store:add-allocation')

    
    def get_context_data(self, **kwargs):
        """
            get
        """
