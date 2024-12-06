from litter.uploader import *
import click

uploader_classes = {
    "catbox": CatboxUploader,
    "litterbox": LitterboxUploader,
}


@click.command()
@click.option("-h", "--host", default="litterbox", help="catbox/litterbox")
@click.option("-t", "--time", help="duration (only for litterbox): 1h/12h/24h/72h")
@click.argument("file")
def upload(host, file, time):
    try:
        uploader_class = uploader_classes[host]

        if host == "litterbox":
            uploader_instance = uploader_class(file, time)
        elif host == "catbox":
            uploader_instance = uploader_class(file)
        else:
            print("choose either catbox/litterbox as host")
            
        result = uploader_instance.execute()
        print(f"\nYour link : {result}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    upload()
