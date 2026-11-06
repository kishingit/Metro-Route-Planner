def linear_search_by_name(stations_list, query_name):
    """Linear Search to find station by name or partial name."""
    query_name = query_name.lower().strip()
    matches = []
    for station in stations_list:
        if query_name in station.name.lower():
            matches.append(station)
    return matches

def binary_search_by_id(sorted_stations, target_id):
    """Binary Search for station by integer ID (requires list sorted by ID)."""
    low = 0
    high = len(sorted_stations) - 1
    
    while low <= high:
        mid = (low + high) // 2
        mid_id = sorted_stations[mid].station_id
        if mid_id == target_id:
            return sorted_stations[mid]
        elif mid_id < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return None

def merge_sort(stations_list, key_func=lambda s: s.name, reverse=False):
    """Merge Sort algorithm (O(N log N)) for sorting station lists."""
    if len(stations_list) <= 1:
        return stations_list

    mid = len(stations_list) // 2
    left = merge_sort(stations_list[:mid], key_func, reverse)
    right = merge_sort(stations_list[mid:], key_func, reverse)

    return _merge(left, right, key_func, reverse)

def _merge(left, right, key_func, reverse):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_val = key_func(left[i])
        right_val = key_func(right[j])

        condition = (left_val > right_val) if reverse else (left_val <= right_val)
        if condition:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
