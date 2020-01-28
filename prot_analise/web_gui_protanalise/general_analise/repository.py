def count_data_in_cellular_details(query, group):
    result = {}
    proteins = {}
    for cluster in query.clusters.all():
        cluster_name = cluster
        result[cluster_name] = {}
        proteins[cluster_name] = {}
        for region in cluster.regions.all():
            if group == 'kingdom':
                kingdom_statistic(cluster_name, proteins, region, result)
            elif group == 'species':
                species_statistic(cluster_name, proteins, region, result)
            elif group == 'proteins':
                proteins_statistic(cluster_name, proteins, region, result)
    for cluster, prot_data in proteins.items():
        for cell, proteins in prot_data.items():
            result[cluster][cell]["protein"] = len(set(proteins))
    return result


def kingdom_statistic(cluster_name, proteins, region, result):
    cell = region.protein.organism.group.name
    if cell not in result[cluster_name].keys():
        result[cluster_name][cell] = {"region": 1}
        proteins[cluster_name][cell] = [region.protein.protein_id]
    else:
        result[cluster_name][cell]["region"] += 1
        proteins[cluster_name][cell].append(region.protein.protein_id)


def species_statistic(cluster_name, proteins, region, result):
    cell = region.protein.organism
    if cell not in result[cluster_name].keys():
        result[cluster_name][cell] = {"region": 1}
        proteins[cluster_name][cell] = [region.protein.protein_id]
    else:
        result[cluster_name][cell]["region"] += 1
        proteins[cluster_name][cell].append(region.protein.protein_id)


def proteins_statistic(cluster_name, proteins, region, result):
    cell = region.protein.protein_id
    if cell not in result[cluster_name].keys():
        result[cluster_name][cell] = {"region": 1}
        proteins[cluster_name][cell] = [region.protein.protein_id]
    else:
        result[cluster_name][cell]["region"] += 1
        proteins[cluster_name][cell].append(region.protein.protein_id)


def count_home_data_details(query):
    res = {}
    for load in query.all():
        first_clust = None
        first_king = None
        regions = []
        proteins = []
        res[load.pk] = {"time": load.load_time}
        for cluster in load.clusters.all():
            if first_clust is None:
                first_clust = cluster.pk
            for region in cluster.regions.all():
                regions.append(region.pk)
                prot = region.protein.protein_id
                proteins.append(prot)
                if first_king is None:
                    first_king = region.protein.organism.group.name
        res[load.pk]["prot_size"] = len(set(proteins))
        res[load.pk]["region_size"] = len(set(regions))
        res[load.pk]["url"] = "/" + str(load.pk) + "/kingdom/" + str(first_king) + "/" + str(first_clust)
    return res
