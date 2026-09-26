import json

def load_users():
    with open('users.json', 'r') as file:
        users_data = json.load(file)
        return users_data


def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)


def load_events():
    with open('events.json', 'r') as file:
        return json.load(file)


def save_events(events):
    with open('events.json', 'w') as file:
        json.dump(events, file, indent=4)


def merge_sort(events,l,h,getter="get_name",order="ascending"):
    if l >= h:
        return
    mid = (l+h)//2
    merge_sort(events,l,mid,getter,order)
    merge_sort(events,mid+1,h,getter,order)
    merge(events,l,mid,h,getter,order)


def merge(events,l,mid,h,getter,order):
    merged = []
    i,j=l,mid+1
    while i<=mid and j<=h:
        val1=getattr(events[i],getter)()
        val2=getattr(events[j],getter)()
        if isinstance(val1,str):
            val1=val1.strip().lower()
            val2=val2.strip().lower()
        if order=="ascending":
            condition= val1<=val2
        else:
            condition = val1>=val2
        if condition:
            merged.append(events[i])
            i += 1
        else:
            merged.append(events[j])
            j += 1
    if i>mid:
        for k in range(j,h+1):
            merged.append(events[k])
    else:
        for k in range(i,mid+1):
            merged.append(events[k])
    for k in range(len(merged)):
        events[l+k] = merged[k]


def binary_search(events, target, getter="get_name"):
    if isinstance(target, str):
        target=target.strip().lower()
    low=0
    high=len(events)-1
    while low<=high:
        mid=(low+high)//2
        mid_value = getattr(events[mid],getter)()
        if isinstance(mid_value, str):
            mid_value=mid_value.strip().lower()
        if mid_value==target:
            return mid
        elif target<mid_value:
            high=mid-1
        else:
            low=mid+1
    return -1
