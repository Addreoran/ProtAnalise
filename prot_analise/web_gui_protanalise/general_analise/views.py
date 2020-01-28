import re

from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import generic

from general_analise.forms import GetData
from general_analise.repository import count_data_in_cellular_details, count_home_data_details
from prot_analise.scripts.menage_data import AllData
from .models import Load, Cluster, Protein, Kingdom, Organism, Database, Region, New


class HomeView(generic.TemplateView):
    template_name = 'general_analise/home.html'


class ContactView(generic.TemplateView):
    template_name = 'general_analise/contact.html'


class AboutView(generic.TemplateView):
    template_name = 'general_analise/about.html'


class NewsView(generic.ListView):
    template_name = 'general_analise/news.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        queryset = New.objects.all()
        return queryset


class LoadsView(generic.ListView):
    template_name = 'general_analise/load.html'
    context_object_name = 'load_list'

    def get_queryset(self):
        load = Load.objects.prefetch_related(
            'clusters'
        ).prefetch_related(
            'clusters__regions'
        ).prefetch_related(
            'clusters__regions__protein'
        ).prefetch_related(
            'clusters__regions__protein__organism'
        ).prefetch_related(
            'clusters__regions__protein__organism__group'

        )
        return count_home_data_details(load)


class FormView(generic.FormView):
    template_name = 'general_analise/index.html'
    form_class = GetData
    success_url = '/{id}/kingdom/{kingdom}/{cluster_pk}'

    def form_valid(self, form):
        self.sender_data = form.send_data()
        self.parse_data()
        load_id, kingdom_name, cluster_pk = self.save_to_database()
        return HttpResponseRedirect(self.success_url.format(id=load_id, kingdom=kingdom_name, cluster_pk=cluster_pk))

    def parse_data(self):
        self.clusters = {}
        patterns = re.compile(self.sender_data['cluster_header'])
        matches = patterns.findall(self.sender_data['data'])
        self.data = self.sender_data['data']
        if matches:
            for match in range(len(matches) - 1):
                new_data = AllData()
                new_data.get_path(data=self.data.split(matches[match])[1].split(matches[match + 1])[0])
                new_data.get_group_taxonomy()
                self.clusters[matches[match]] = new_data

            new_data = AllData()
            new_data.get_path(data=self.data.split(matches[-1])[1])
            new_data.get_group_taxonomy()
            self.clusters[matches[-1]] = new_data
        else:
            new_data = AllData()
            new_data.get_path(data=self.data)
            new_data.get_group_taxonomy()
            self.clusters[">one;"] = new_data

    def save_to_database(self):
        new_load = Load()
        new_load.load_time = timezone.now()
        new_load.save()
        for cluster_name, cluster in self.clusters.items():
            new_cluster = Cluster()
            new_cluster.name = cluster_name
            new_cluster.load_number = new_load
            new_cluster.save()
            for i in cluster.proteins.items():
                organisms = cluster.get_species_by_prot_id(i[0])
                king = cluster.get_kingdom_by_prot_id(i[0])
                try:
                    is_prot = Protein.objects.get(protein_id=i[0])
                    cellurarity = Kingdom.objects.get(name=king)
                except:
                    try:
                        cellurarity = Kingdom.objects.get(name=king)
                    except:
                        cellurarity = Kingdom()
                        cellurarity.name = king
                        cellurarity.save()
                    try:
                        organis = Organism.objects.get(organism=organisms)
                    except:
                        organis = Organism()
                        organis.organism = organisms
                        organis.group = cellurarity
                        organis.save()
                    is_prot = Protein()
                    is_prot.protein_id = i[0]
                    is_prot.sequece_len = cluster.lengths[i[0]]
                    is_prot.sequece = cluster.sequences[i[0]]
                    is_prot.database = Database.objects.get(name=self.sender_data['database'])
                    is_prot.organism = organis
                    is_prot.save()
                for regions in i[1]:
                    try:
                        is_reg = Region.objects.get(protein=is_prot, begin=regions.begin, end=regions.end,
                                                    header=regions.header)
                    except:
                        is_reg = Region()
                        is_reg.protein = is_prot
                        is_reg.begin = regions.begin
                        is_reg.end = regions.end
                        is_reg.save()
                    new_cluster.regions.add(is_reg)
                    new_cluster.save()
        return new_load.pk, cellurarity.name, new_cluster.pk


class DetailCellularView(generic.DetailView):
    model = Load
    template_name = 'general_analise/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        stats = count_data_in_cellular_details(self.object, kwargs['group'])
        context = self.get_context_data(
            object=self.object,
            stat=stats,
            **kwargs,
        )
        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            'clusters'
        ).prefetch_related(
            'clusters__regions'
        ).prefetch_related(
            'clusters__regions__protein'
        ).prefetch_related(
            'clusters__regions__protein__organism'
        ).prefetch_related(
            'clusters__regions__protein__organism__group'

        )
        return queryset
