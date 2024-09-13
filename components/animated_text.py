from pyreact import component

@component
def animated_text(props):
    return f"""

<div class="container">
  <div>
    <h1 class="type">{props.get('text','Hello World!')}</h1>
  </div>
</div>

"""