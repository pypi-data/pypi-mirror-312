import rich_click as click
from string import ascii_lowercase, digits
from novara.utils import logger
from novara.request import request, JSONDecodeError
from random import choices
from io import BytesIO
from questionary import confirm, select, path
from zipfile import ZipFile
import os
import shutil
from novara.config import config


def get_service():
    r = request.get("api/services/")
    if not r.ok:
        raise click.ClickException(
            f"Failed requesting list of services from remote with error: {r.text}"
        )
        exit()
    try:
        services = r.json()
    except JSONDecodeError:
        raise click.ClickException(
            f"failed to decode response as json: {r.text[:20] if len(r.text) > 20 else r.text}"
        )

    service = select("Please select a service", choices=services).ask()
    print(service)

    return service


@click.command()
@click.option(
    "-s",
    "--service",
    default=None,
    help="the name of the service the exploit will be attacking",
)
@click.option(
    "-n", "--name", default=None, help="the internal name for the exploit identifing it"
)
@click.option("-a", "--author", default=None, help="name of the exploit's author")
@click.option(
    "-d",
    "--directory",
    default=None,
    help="specify a different directory to put the exploit",
)
def init(service, name, author, directory):
    """Initialize a new exploit from a template"""

    # Priority: CLI argument > Environment variable > Prompt

    service = service or get_service()
    name = name or "".join(choices(ascii_lowercase + digits, k=6))
    author = (
        author
        or config.author
        or os.environ.get("AUTHOR")
        or click.prompt("Please enter this exploit author's name")
    )

    # -----------------------------------------------------------------

    if directory and directory[0] != "/":
        directory = os.path.join(os.getcwd(), directory)
    else:
        directory = path("Where should the exploied be saved to?", default=os.path.join(os.getcwd(), f'{service}-{name}'), only_directories=True).ask()
    
    if os.path.exists(directory) and len(os.listdir(directory)) > 0:
        logger.warning(f"The Path '{directory}' is not empty!")

        if confirm("Do you want to overwrite the directory?").ask():
            shutil.rmtree(directory)
        else:
            logger.info("Directory won't be overwritten, exiting...")
            exit()
    
    logger.info(f"setting up directory: {directory}")
    logger.info("requesting template")

    r = request.post(
        f"api/services/{service}/template/",
        params={"exploit_name": name, "exploit_author": author, "additional_args": ""},
    )
    if not r.ok:
        raise click.ClickException(
            f"Requesting template from remote failed with error: {r.text}. Did you run novara configure?"
        )

    logger.info("extracting template")
    zip_template = BytesIO(r.content)
    os.mkdir(directory)
    with ZipFile(zip_template) as zip:
        zip.extractall(directory)

    logger.info(f"Template extracted sucessfully into directory {directory or f'{service}-{name}'}")
    logger.info("To add a new dependency run 'novara generate'")
    logger.info("To run the current exploit run 'novara run [local|remote]'")
    logger.info("Happy exploiting!")
