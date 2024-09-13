from pyreact import pyreact, component, route
from components.animated_text import animated_text as at
from components.image import img

##################################################################################################################
# Once your app is fully set up, you can run this script to verify whether it's functioning correctly.
#This will help ensure everything is working as expected before further development.
##################################################################################################################



@component
def App(props):
    return f"""{img(src='/pyreact-logo',alt='PyReact Logo')}
{at(text='PyReact app running')}

"""

@route("/pyreact-logo")
async def logo(request):
    with open("static/PyReact-logo.png", "rb") as image:
        logo = image.read()
        return await pyreact.send_file(logo, "PyReact-logo.png")


@route("/")
async def index(request):
    return App()


# Initialize PyReact app
app = pyreact.create_app()
pyreact.set_static_dir("static")
pyreact.add_global_css_file("styles.css")
pyreact.set_mode("build")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=3000, reload=True)
