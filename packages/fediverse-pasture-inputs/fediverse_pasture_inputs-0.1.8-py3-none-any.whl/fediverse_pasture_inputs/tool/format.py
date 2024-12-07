import json

from fediverse_pasture_inputs.types import InputData

from .transformer import ExampleTransformer


def write_json(fp, data):
    fp.write("```json\n")
    fp.write(json.dumps(data, indent=2, sort_keys=True))
    fp.write("\n```\n\n")


async def page_from_inputs(fp, inputs: InputData):
    transformer = ExampleTransformer()

    fp.write(f"# {inputs.title}\n\n")
    fp.write(inputs.frontmatter)

    fp.write("\n\n## Objects \n\n")

    for idx, ex in enumerate(inputs.examples):
        fp.write(f"\n### Object {idx+1}\n\n")
        write_json(fp, await transformer.create_object(ex))

    fp.write("\n\n## Activities \n\n")

    for idx, ex in enumerate(inputs.examples):
        fp.write(f"\n### Activity {idx+1}\n\n")
        write_json(fp, await transformer.create_activity(ex))
