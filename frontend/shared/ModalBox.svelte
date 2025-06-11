<script lang="ts">
	import { BaseColorPicker } from "@gradio/colorpicker";
    import { BaseButton } from "@gradio/button";
    import { BaseDropdown, BaseMultiselect } from "./patched_dropdown/Index.svelte";
    import { BaseTextbox } from "@gradio/textbox";
	import { createEventDispatcher } from "svelte";
    import { onMount, onDestroy } from "svelte";

    export let name = "";
    export let currentName = "";

    export let label = [];
    export let currentLabel = [];
    export let choices = [];  // [(label, i)]

    export let secondLabel = "";
    export let currentSecondLabel = '';
    export let secondChoices = [];  // [(label, i)]

    export let thirdLabel = [];
    export let currentThirdLabel = [];
    export let thirdChoices = [];  // [(label, i)]

    export let fourthLabel = [];
    export let currentFourthLabel = [];
    export let fourthChoices = [];  // [(label, i)]

    export let startScale = "1.0";
    export let currentStartScale = "1.0";

    export let endScale = "1.0";
    export let currentEndScale = "1.0";
    
    export let choicesColors = [];
    export let color = "";
    export let currentColor = "";
    export let showRemove = true;
    
    const dispatch = createEventDispatcher<{
		change: object;
	}>();

    function dispatchChange(ret: number) {
        dispatch("change", {
            label: currentLabel,
            secondLabel: currentSecondLabel,
            thirdLabel: currentThirdLabel,
            fourthLabel: currentFourthLabel,
            color: currentColor,
            name: currentName,
            startScale: currentStartScale,
            endScale: currentEndScale,
            ret: ret // -1: remove, 0: cancel, 1: change
        });
    }

    function onTextboxChange(event) {
        const { detail } = event;
		let choice = detail;
        currentName = choice;
    }

    function onStartScaleChange(event) {
        const { detail } = event;
		let choice = detail;
        currentStartScale = choice;
    }

    function onEndScaleChange(event) {
        const { detail } = event;
		let choice = detail;
        currentEndScale = choice;
    }

    function onDropDownChange(event) {
        const { detail } = event;
		let choice = detail;

        if (Number.isInteger(choice)) {
            if (Array.isArray(choicesColors) && choice < choicesColors.length) {
                currentColor = choicesColors[choice];
            }
            if (Array.isArray(choices) && choice < choices.length) {
                currentLabel = choices[choice][0];
            }
        } else {
            currentLabel = choice;
        }
    }

    function onSecondDropDownChange(event) {
        const { detail } = event;
		let choice = detail;

        if (Number.isInteger(choice)) {
            if (Array.isArray(secondChoices) && choice < secondChoices.length) {
                currentSecondLabel = secondChoices[choice][0];
            }
        } else {
            currentSecondLabel = choice;
        }
    }

    function onThirdDropDownChange(event) {
        const { detail } = event;
		let choice = detail;
        
        if (Number.isInteger(choice)) {
            if (Array.isArray(thirdChoices) && choice < thirdChoices.length) {
                currentThirdLabel = thirdChoices[choice][0];
            }
        } else {
            currentThirdLabel = choice;
        }
    }

    function onFourthDropDownChange(event) {
        const { detail } = event;
		let choice = detail;
        
        if (Number.isInteger(choice)) {
            if (Array.isArray(fourthChoices) && choice < fourthChoices.length) {
                currentFourthLabel = fourthChoices[choice][0];
            }
        } else {
            currentFourthLabel = choice;
        }
    }

    function onColorChange(event) {
        const { detail } = event;
		currentColor = detail;
    }

    function onDropDownEnter(event) {
        onDropDownChange(event);
        dispatchChange(1);
    }

    function onSecondDropDownEnter(event) {
        onSecondDropDownChange(event);
        dispatchChange(1);
    }

    function onThirdDropDownEnter(event) {
        onThirdDropDownChange(event);
        dispatchChange(1);
    }

    function onFourthDropDownEnter(event) {
        onFourthDropDownChange(event);
        dispatchChange(1);
    }

    function handleKeyPress(event: KeyboardEvent) {
		switch (event.key) {
			case "Enter":
                dispatchChange(1);
				break;
		}
	}

	onMount(() => {
		document.addEventListener("keydown", handleKeyPress);
        currentLabel = label;
        currentSecondLabel = secondLabel;
        currentThirdLabel = thirdLabel;
        currentFourthLabel = fourthLabel;
        currentName = name;
        currentColor = color;
        currentStartScale = startScale;
        currentEndScale = endScale;
	});
    
	onDestroy(() => {
        document.removeEventListener("keydown", handleKeyPress);
  	});

</script>

<div class="modal" id="model-box-edit">
    <div class="modal-container">
        <div class="model-content">
            <div style="margin-right: 10px; margin-top: 10px;">
                <BaseMultiselect
                    value={currentLabel}
                    label="Content Label(内容标签)"
                    {choices}
                    show_label={true}
                    allow_custom_value={false}
                    on:change={onDropDownChange}
                    on:enter={onDropDownEnter}
                />
            </div>
            <div style="margin-right: 10px; margin-top: 10px;">
                <BaseDropdown
                    value={currentSecondLabel}
                    label="Layout Label(层级标签)"
                    choices={secondChoices}
                    show_label={true}
                    allow_custom_value={false}
                    on:change={onSecondDropDownChange}
                    on:enter={onSecondDropDownEnter}
                />
            </div>
            <div style="margin-right: 10px; margin-top: 10px;">
                <BaseMultiselect
                    value={currentThirdLabel}
                    label="Lens Label(镜头标签)"
                    choices={thirdChoices}
                    show_label={true}
                    allow_custom_value={false}
                    on:change={onThirdDropDownChange}
                    on:enter={onThirdDropDownEnter}
                />
            </div>
            <div style="margin-right: 10px; margin-top: 10px;">
                <BaseMultiselect
                    value={currentFourthLabel}
                    label="Function Label(功能标签)"
                    choices={fourthChoices}
                    show_label={true}
                    allow_custom_value={false}
                    on:change={onFourthDropDownChange}
                    on:enter={onFourthDropDownEnter}
                />
            </div>
            <div style="margin-right: 10px;">
                <BaseTextbox
                    value={name}
                    label="Name"
                    show_label={true}
                    on:change={onTextboxChange}
                />
            </div>
            <div style="margin-right: 10px;">
                <BaseTextbox
                    value={startScale}
                    label="Start Scale"
                    show_label={true}
                    on:change={onStartScaleChange}
                />
            </div>
            <div style="margin-right: 10px;">
                <BaseTextbox
                    value={endScale}
                    label="End Scale"
                    show_label={true}
                    on:change={onEndScaleChange}
                />
            </div>
            <div style="margin-right: 40px; margin-bottom: 8px; margin-top: 10px;">
                <BaseColorPicker
                    value={currentColor}
                    label="Color"
                    show_label={true}
                    on:change={onColorChange}
                />
            </div>
            <div style="display: flex; align-items: center; justify-content: center; margin-top: 20px;">
                <div style="margin-right: 8px;">
                    <BaseButton
                    on:click={() => dispatchChange(0)}
                    >Cancel</BaseButton>
                </div>
                {#if showRemove}
                    <div style="margin-right: 8px;">
                        <BaseButton
                            variant="stop"
                            on:click={() => dispatchChange(-1)}
                        >Remove</BaseButton>
                    </div>
                {/if}
                <div>
                    <BaseButton
                        variant="primary"
                        on:click={() => dispatchChange(1)}
                    >OK</BaseButton>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .modal {
        position: fixed;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        z-index: var(--layer-top);
        -webkit-backdrop-filter: blur(4px);
        backdrop-filter: blur(4px);
    }

    .modal-container {
        border-style: solid;
        border-width: var(--block-border-width);
        border-color: var(--block-border-color);
        margin-top: 10%;
        padding: 20px;
        box-shadow: var(--block-shadow);
        border-color: var(--block-border-color);
        border-radius: var(--block-radius);
        background: var(--block-background-fill);
        position: fixed;
        left: 50%;
        transform: translateX(-50%);
        width: fit-content;
    }

    .model-content {
        display: block;
        align-items: baseline;
    }

    /* .model-content {
        display: flex;
        align-items: flex-end;
    } */
</style>
