from pyreact import component

@component
def img(props):
    return f"""<img src="{props.get('src', '')}" alt="{props.get('alt', '')}"/>"""
