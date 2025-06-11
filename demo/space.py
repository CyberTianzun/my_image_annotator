
import gradio as gr
from app import demo as app
import os

_docs = {'my_image_annotator': {'description': 'Creates a component to displays a base image and colored annotations on top of that image. Annotations can take the from of rectangles (e.g. object detection) or masks (e.g. image segmentation).\nAs this component does not accept user input, it is rarely used as an input component.\n', 'members': {'__init__': {'value': {'type': 'dict | None', 'default': 'None', 'description': "A dict or None. The dictionary must contain a key 'image' with either an URL to an image, a numpy image or a PIL image. Optionally it may contain a key 'boxes' with a list of boxes. Each box must be a dict wit the keys: 'xmin', 'ymin', 'xmax' and 'ymax' with the absolute image coordinates of the box. Optionally can also include the keys 'label' and 'color' describing the label and color of the box. Color must be a tuple of RGB values (e.g. `(255,255,255)`)."}, 'boxes_alpha': {'type': 'float | None', 'default': 'None', 'description': 'Opacity of the bounding boxes 0 and 1.'}, 'label_list': {'type': 'list[str] | None', 'default': 'None', 'description': 'List of valid labels.'}, 'second_label_list': {'type': 'list[str] | None', 'default': 'None', 'description': None}, 'third_label_list': {'type': 'list[str] | None', 'default': 'None', 'description': None}, 'fourth_label_list': {'type': 'list[str] | None', 'default': 'None', 'description': None}, 'label_colors': {'type': 'list[str] | None', 'default': 'None', 'description': 'Optional list of colors for each label when `label_list` is used. Colors must be a tuple of RGB values (e.g. `(255,255,255)`).'}, 'box_min_size': {'type': 'int | None', 'default': 'None', 'description': 'Minimum valid bounding box size.'}, 'handle_size': {'type': 'int | None', 'default': 'None', 'description': 'Size of the bounding box resize handles.'}, 'box_thickness': {'type': 'int | None', 'default': 'None', 'description': 'Thickness of the bounding box outline.'}, 'box_selected_thickness': {'type': 'int | None', 'default': 'None', 'description': 'Thickness of the bounding box outline when it is selected.'}, 'disable_edit_boxes': {'type': 'bool | None', 'default': 'None', 'description': 'Disables the ability to set and edit the label and color of the boxes.'}, 'single_box': {'type': 'bool', 'default': 'False', 'description': 'If True, at most one box can be drawn.'}, 'height': {'type': 'int | str | None', 'default': 'None', 'description': 'The height of the displayed image, specified in pixels if a number is passed, or in CSS units if a string is passed.'}, 'width': {'type': 'int | str | None', 'default': 'None', 'description': 'The width of the displayed image, specified in pixels if a number is passed, or in CSS units if a string is passed.'}, 'image_mode': {'type': '"1"\n    | "L"\n    | "P"\n    | "RGB"\n    | "RGBA"\n    | "CMYK"\n    | "YCbCr"\n    | "LAB"\n    | "HSV"\n    | "I"\n    | "F"', 'default': '"RGB"', 'description': '"RGB" if color, or "L" if black and white. See https://pillow.readthedocs.io/en/stable/handbook/concepts.html for other supported image modes and their meaning.'}, 'sources': {'type': 'list["upload" | "webcam" | "clipboard"] | None', 'default': '["upload", "webcam", "clipboard"]', 'description': 'List of sources for the image. "upload" creates a box where user can drop an image file, "webcam" allows user to take snapshot from their webcam, "clipboard" allows users to paste an image from the clipboard. If None, defaults to ["upload", "webcam", "clipboard"].'}, 'image_type': {'type': '"numpy" | "pil" | "filepath"', 'default': '"numpy"', 'description': 'The format the image is converted before being passed into the prediction function. "numpy" converts the image to a numpy array with shape (height, width, 3) and values from 0 to 255, "pil" converts the image to a PIL image object, "filepath" passes a str path to a temporary file containing the image. If the image is SVG, the `type` is ignored and the filepath of the SVG is returned.'}, 'label': {'type': 'list | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'True', 'description': 'if True, will allow users to upload and annotate an image; if False, can only be used to display annotated images.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'show_download_button': {'type': 'bool', 'default': 'True', 'description': 'If True, will show a button to download the image.'}, 'show_share_button': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.'}, 'show_clear_button': {'type': 'bool | None', 'default': 'True', 'description': 'If True, will show a button to clear the current image.'}, 'show_remove_button': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will show a button to remove the selected bounding box.'}, 'handles_cursor': {'type': 'bool | None', 'default': 'True', 'description': 'If True, the cursor will change when hovering over box handles in drag mode. Can be CPU-intensive.'}}, 'postprocess': {'value': {'type': 'dict | None', 'description': 'A dict with an image and an optional list of boxes or None.'}}, 'preprocess': {'return': {'type': 'dict | None', 'description': 'A dict with the image and boxes or None.'}, 'value': None}}, 'events': {'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the my_image_annotator using the clear button for the component.'}, 'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the my_image_annotator changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the my_image_annotator.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'my_image_annotator': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_my_image_annotator`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_my_image_annotator
```

## Usage

```python
import gradio as gr
from gradio_my_image_annotator import my_image_annotator


example_annotation = {
    # "image": "https://gradio-builds.s3.amazonaws.com/demo-files/base.png",
    "image": "/Users/hiro/online/logic/my_image_annotator/demo/map1_block5_diaoyudi1_front_s.show.png",
    "boxes": [
        {
            "xmin": 405,
            "ymin": 62,
            "xmax": 1056,
            "ymax": 413,
            "label": ["Person"],
            "secondLabel": 'Test2',
            "thirdLabel": ["Banana"],
            "fourthLabel": ["Cat"],
            "color": (0, 0, 255),
            "name": "xxx",
            "startScale": "0.0",
            "endScale": "0.0",
            "isLine": True,
            "points": [[959.296875, 855.47265625], [959.296875, 854.48046875], [959.296875, 852.6328125], [959.296875, 850.9765625], [959.296875, 847.25], [959.296875, 844.8671875], [959.296875, 841.71484375], [959.296875, 838.07421875], [959.1015625, 833.49609375], [958.6953125, 828.00390625], [958.203125, 822.19140625], [957.46484375, 816.26953125], [956.453125, 809.8671875], [955.40234375, 803.71875], [954.5859375, 798.5625], [953.7890625, 793.546875], [953.06640625, 789.76953125], [952.1484375, 786.171875], [951.23046875, 782.91796875], [950.53515625, 780.21484375], [949.4921875, 777.3984375], [948.47265625, 774.90234375], [947.63671875, 772.4296875], [946.87890625, 770.5078125], [946.18359375, 769.109375], [945.5, 767.7421875], [944.84375, 766.5859375], [944.38671875, 765.828125], [944.15234375, 765.26953125], [943.7734375, 764.38671875], [943.20703125, 763.03125], [942.61328125, 761.81640625], [942.11328125, 761.16015625], [941.51171875, 760.40234375], [940.98828125, 759.51171875], [940.61328125, 758.86328125], [940.04296875, 758.0703125], [939.24609375, 757.09375], [938.5546875, 756.09375], [937.890625, 755.2578125], [936.9453125, 754.71484375], [936.171875, 754.23828125], [935.71875, 753.8125], [934.81640625, 753.10546875], [933.0625, 751.734375], [930.77734375, 750.078125], [928.98828125, 748.71484375], [928.00390625, 747.88671875], [926.609375, 747.015625], [923.11328125, 744.40234375], [921.95703125, 743.5234375], [920.65234375, 742.5625], [919.4140625, 741.6640625], [918.37890625, 740.953125], [917.34375, 740.25], [916.48828125, 739.59765625], [915.66796875, 739.09375], [914.72265625, 738.58984375], [913.91796875, 738.109375], [913.14453125, 737.78125], [912.19921875, 737.4453125], [911.22265625, 737.109375], [910.4375, 736.80078125], [909.8046875, 736.49609375], [909.1875, 736.19140625], [908.765625, 736.04296875], [908.34375, 735.89453125], [908.046875, 735.6171875], [907.7578125, 735.34375], [907.18359375, 735.19921875], [906.42578125, 734.8828125], [905.484375, 734.41015625], [904.73046875, 734.15625], [904.1171875, 733.8046875], [903.33984375, 733.37890625], [902.57421875, 733.046875], [901.94140625, 732.73046875], [901.328125, 732.546875], [900.80078125, 732.36328125], [900.48046875, 732.2109375], [900.21875, 732.078125], [899.921875, 731.9453125], [899.67578125, 731.9453125], [899.2890625, 731.80859375], [898.546875, 731.515625], [897.5859375, 731.19140625], [896.41015625, 730.8515625], [895.25, 730.67578125], [894.09375, 730.33203125], [893.125, 729.98828125], [892.3671875, 729.828125], [891.73046875, 729.5859375], [891.30078125, 729.47265625], [890.86328125, 729.421875], [890.53515625, 729.39453125], [890.21484375, 729.3828125], [889.9140625, 729.375], [889.64453125, 729.37109375]],
        },
        {
            "xmin":2594,
            "ymin":1343,
            "xmax":3238,
            "ymax":1875,
            "label": ["Person"],
            "thirdLabel": ["Apple"],
            "fourthLabel": ["Dog"],
            "secondLabel": 'Test',
            "color": (0, 255, 0),
            "name": "222",
            "startScale": "0.0",
            "endScale": "0.0",
            "isLine": True,
            "points": [[3237,1874], [2595,1358]],
        },
        
    ]
}

def get_boxes_json(annotations):
    return annotations["boxes"]


with gr.Blocks() as demo:
    with gr.Tab("Object annotation", id="tab_object_annotation"):
        annotator = my_image_annotator(
            example_annotation,
            label_list=["Person", "Vehicle"],
            second_label_list=["Test", "Test2", "Test3"],
            third_label_list=["Apple", "Banana"],
            fourth_label_list=["Dog", "Cat"],
            label_colors=[(0, 255, 0), (255, 0, 0)],
        )
        button_get = gr.Button("Get bounding boxes")
        json_boxes = gr.JSON()
        button_get.click(get_boxes_json, annotator, json_boxes)


if __name__ == "__main__":
    demo.launch()
```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `my_image_annotator`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["my_image_annotator"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["my_image_annotator"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, a dict with the image and boxes or None.
- **As output:** Should return, a dict with an image and an optional list of boxes or None.

 ```python
def predict(
    value: dict | None
) -> dict | None:
    return value
```
""", elem_classes=["md-custom", "my_image_annotator-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          my_image_annotator: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
