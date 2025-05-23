<script lang="ts">
    import { onMount, onDestroy, createEventDispatcher } from "svelte";
	import { BoundingBox, Hand, Trash, Line } from "./icons/index";
	import ModalBox from "./ModalBox.svelte";
	import Box from "./Box";
	import { Colors } from './Colors.js';
	import AnnotatedImageData from "./AnnotatedImageData";

	enum Mode {creation, drag, creationLine}

    export let imageUrl: string | null = null;
	export let interactive: boolean;
	export let boxAlpha = 0.5;
	export let boxMinSize = 25;
	export let handleSize: number;
	export let boxThickness: number;
	export let boxSelectedThickness: number;
	export let value: null | AnnotatedImageData;
	export let choices = [];
    export let choicesColors = [];
	export let disableEditBoxes: boolean = false;
	export let height: number | string = "100%";
	export let width: number | string = "100%";
	export let singleBox: boolean = false;
	export let showRemoveButton: boolean = null;
	export let handlesCursor: boolean = true;

	if (showRemoveButton === null) {
		showRemoveButton = (disableEditBoxes);
	}

    let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D;
    let image = null;
	let selectedBox = -1;
	let mode: Mode = Mode.drag;

	if (value !== null && value.boxes.length == 0) {
		mode = Mode.creation;
	}

	let canvasXmin = 0;
	let canvasYmin = 0;
	let canvasXmax = 0;
	let canvasYmax = 0;
	let scaleFactor = 1.0;

	let imageWidth = 0;
	let imageHeight = 0;

	let editModalVisible = false;
	let newModalVisible = false;

	const dispatch = createEventDispatcher<{
		change: undefined;
	}>();

	function colorHexToRGB(hex: string) {
		var r = parseInt(hex.slice(1, 3), 16),
			g = parseInt(hex.slice(3, 5), 16),
			b = parseInt(hex.slice(5, 7), 16);
		return "rgb(" + r + ", " + g + ", " + b + ")";
	}

	function colorRGBAToHex(rgba: string) {
		const rgbaValues = rgba.match(/(\d+(\.\d+)?)/g);
		const r = parseInt(rgbaValues[0]);
		const g = parseInt(rgbaValues[1]);
		const b = parseInt(rgbaValues[2]);
		const hex = "#" + ((1 << 24) | (r << 16) | (g << 8) | b).toString(16).slice(1);
		return hex;
	}
	
    function draw() {
		if (ctx) {
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			if (image !== null){
				ctx.drawImage(image, canvasXmin, canvasYmin, imageWidth, imageHeight);
			}
			for (const box of value.boxes.slice().reverse()) {
				box.render(ctx);
			}
		}
	}

    function selectBox(index: number) {
		selectedBox = index;
		value.boxes.forEach(box => {box.setSelected(false);});
		if (index >= 0 && index < value.boxes.length){
			value.boxes[index].setSelected(true);
		}
		draw();
	}

	function handlePointerDown(event: PointerEvent) {
		if (!interactive) {
			return;
		}

		if (
			event.target instanceof Element &&
			event.target.hasPointerCapture(event.pointerId)
		) {
			event.target.releasePointerCapture(event.pointerId);
		}

		if (mode === Mode.creation) {
			createBox(event, false);
		} else if (mode === Mode.creationLine) {
			createBox(event, true);
		} else if (mode === Mode.drag) {
			clickBox(event);
		}
	}

	function clickBox(event: PointerEvent) {
		const rect = canvas.getBoundingClientRect();
		const mouseX = event.clientX - rect.left;
		const mouseY = event.clientY - rect.top;

		// Check if the mouse is over any of the resizing handles
		for (const [i, box] of value.boxes.entries()) {
			const handleIndex = box.indexOfPointInsideHandle(mouseX, mouseY);
			if (handleIndex >= 0) {
				selectBox(i);
				box.startResize(handleIndex, event);
				return;
			}
		}

		// Check if the mouse is inside a box
		for (const [i, box] of value.boxes.entries()) {
			if (box.isPointInsideBox(mouseX, mouseY)) {
				selectBox(i);
				box.startDrag(event);
				return;
			}
		}

		if (!singleBox) {
			selectBox(-1);
		}
	}

	function handlePointerUp(event: PointerEvent) {
		dispatch("change");
	}

	function handlePointerMove(event: PointerEvent) {
		if (value === null) {
			return;
		}

		if (mode !== Mode.drag) {
			return;
		}

		const rect = canvas.getBoundingClientRect();
		const mouseX = event.clientX - rect.left;
		const mouseY = event.clientY - rect.top;

		for (const [_, box] of value.boxes.entries()) {
			const handleIndex = box.indexOfPointInsideHandle(mouseX, mouseY);
			if (handleIndex >= 0) {
				canvas.style.cursor = box.resizeHandles[handleIndex].cursor;
				return;
			}
		}

		canvas.style.cursor = "default";
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (!interactive) {
			return;
		}

		switch (event.key) {
			case "Delete":
				onDeleteBox();
				break;
		}
	}

	function createBox(event: PointerEvent, isLine: boolean) {
		const rect = canvas.getBoundingClientRect();
		const x = (event.clientX - rect.left - canvasXmin) / scaleFactor;
		const y = (event.clientY - rect.top - canvasYmin) / scaleFactor;
		let color;
		if (choicesColors.length > 0) {
			color = colorHexToRGB(choicesColors[0]);
		} else if (singleBox) {
			if (value.boxes.length > 0) {
				color = value.boxes[0].color;
			} else {
				color = Colors[0];
			}
		} else {
			color = Colors[value.boxes.length % Colors.length];
		}
		
		let box = new Box(
			draw,
			onBoxFinishCreation,
			canvasXmin,
			canvasYmin,
			canvasXmax,
			canvasYmax,
			isLine,
			"",
			"",
			x,
			y,
			x,
			y,
			[],
			color,
			boxAlpha,
			boxMinSize,
			handleSize,
			boxThickness,
			boxSelectedThickness
		);
		box.startCreating(event, rect.left, rect.top);
		if (singleBox) {
			value.boxes = [box];
		} else {
			value.boxes = [box, ...value.boxes];
		}
		selectBox(0);
		draw();
		dispatch("change");
	}

	function setCreateMode() {
		mode = Mode.creation;
		canvas.style.cursor = "crosshair";
	}

	function setCreateLineMode() {
		mode = Mode.creationLine;
		canvas.style.cursor = "crosshair";
	}

	function setDragMode() {
		mode = Mode.drag;
		canvas.style.cursor = "default";
	}

	function onBoxFinishCreation() {
		if (selectedBox >= 0 && selectedBox < value.boxes.length) {
			if (value.boxes[selectedBox].getArea() < 1) {
				onDeleteBox();
			} else {
				if (!disableEditBoxes) {
					newModalVisible = true;
				}
				if (singleBox) {
					setDragMode();
				}
			}
		}
	}

	function onEditBox() {
		if (selectedBox >= 0 && selectedBox < value.boxes.length && !disableEditBoxes) {
			editModalVisible = true;
		}
	}

	function handleDoubleClick(event: MouseEvent){
		if (!interactive) {
			return;
		}
		
		onEditBox();
	}

	function onModalEditChange(event) {
		editModalVisible = false;
		const { detail } = event;
		let name = detail.name;
		let label = detail.label;
		let color = detail.color;
		let ret = detail.ret;
		if (selectedBox >= 0 && selectedBox < value.boxes.length) {
			let box = value.boxes[selectedBox];
			if (ret == 1) {
				box.label = label;
				box.name = name;
				box.color = colorHexToRGB(color);
				draw();
				dispatch("change");
			} else if (ret == -1) {
				onDeleteBox();
			}
		}
	}

	function onModalNewChange(event) {
		newModalVisible = false;
		const { detail } = event;
		let name = detail.name;
		let label = detail.label;
		let color = detail.color;
		let ret = detail.ret;
		if (selectedBox >= 0 && selectedBox < value.boxes.length) {
			let box = value.boxes[selectedBox];
			if (ret == 1) {
				box.label = label;
				box.name = name;
				box.color = colorHexToRGB(color);
				draw();
				dispatch("change");
			} else {
				onDeleteBox();
			}
		}
	}

    function onDeleteBox() {
		if (selectedBox >= 0 && selectedBox < value.boxes.length) {
			value.boxes.splice(selectedBox, 1);
			selectBox(-1);
			if (singleBox) {
				setCreateMode();
			}
			dispatch("change");
		}
	}

	function resize() {
		if (canvas) {
			scaleFactor = 1;
			canvas.width = canvas.clientWidth;
			if (image !== null) {
				if (image.width > canvas.width) {
					scaleFactor = canvas.width / image.width;
					imageWidth = image.width * scaleFactor;
					imageHeight = image.height * scaleFactor;
					canvasXmin = 0;
					canvasYmin = 0;
					canvasXmax = imageWidth;
					canvasYmax = imageHeight;
					canvas.height = imageHeight;
				} else {
					imageWidth = image.width;
					imageHeight = image.height;
					var x = (canvas.width - imageWidth) / 2;
					canvasXmin = x;
					canvasYmin = 0;
					canvasXmax = x + imageWidth;
					canvasYmax = image.height;
					canvas.height = imageHeight;
				}
			} else {
				canvasXmin = 0;
				canvasYmin = 0;
				canvasXmax = canvas.width;
				canvasYmax = canvas.height;
				canvas.height = canvas.clientHeight;
			}
			if (canvasXmax > 0 && canvasYmax > 0){
				for (const box of value.boxes) {
					box.canvasXmin = canvasXmin;
					box.canvasYmin = canvasYmin;
					box.canvasXmax = canvasXmax;
					box.canvasYmax = canvasYmax;
					box.setScaleFactor(scaleFactor);
				}
			}
			draw();
			dispatch("change");
		}
	}
	const observer = new ResizeObserver(resize);

	function parseInputBoxes() {
		for (let i = 0; i < value.boxes.length; i++) {
			let box = value.boxes[i];
			if (!(box instanceof Box)) {
				let color = "";
				let label = "";
				let name = "";
				if (box.hasOwnProperty("color")) {
					color = box["color"];
					if (Array.isArray(color) && color.length === 3) {
            			color = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
        			}
				} else {
					color = Colors[i % Colors.length];
				}
				if (box.hasOwnProperty("label")) {
					label = box["label"];
				}
				if (box.hasOwnProperty("name")) {
					name = box["name"];
				}
				const isLine = box['isLine'] || false;
				let pathPoints = [];
				if (box.hasOwnProperty("points")) {
					pathPoints = box.points;
				}

				box = new Box(
					draw,
					onBoxFinishCreation,
					canvasXmin,
					canvasYmin,
					canvasXmax,
					canvasYmax,
					isLine,
					name,
					label,
					box["xmin"],
					box["ymin"],
					box["xmax"],
					box["ymax"],
					pathPoints,
					color,
					boxAlpha,
					boxMinSize,
					handleSize,
					boxThickness,
					boxSelectedThickness
				);
				value.boxes[i] = box;
			}
		}
	}

	$: {
		value;
		setImage();
		parseInputBoxes();
		resize();
		draw();
	}

	function setImage(){
		if (imageUrl !== null) {
			if (image === null || image.src != imageUrl) {
				image = new Image();
				image.src = imageUrl;
				image.onload = function(){
					resize();
					draw();
				}
			}
		}
	}

	onMount(() => {
		if (Array.isArray(choices) && choices.length > 0) {
			if (!Array.isArray(choicesColors) || choicesColors.length == 0) {
				for (let i = 0; i < choices.length; i++) {
					let color = Colors[i % Colors.length];
					choicesColors.push(colorRGBAToHex(color));
				}
			}
		}

		ctx = canvas.getContext("2d");
		observer.observe(canvas);

		if (selectedBox < 0 && value !== null && value.boxes.length > 0) {
			selectBox(0);
		}
		setImage();
		resize();
		draw();
	});
	
	function handleCanvasFocus() {
		document.addEventListener("keydown", handleKeyPress);
	}
	
	function handleCanvasBlur() {
		document.removeEventListener("keydown", handleKeyPress);
	}

	onDestroy(() => {
		document.removeEventListener("keydown", handleKeyPress);
  	});

</script>

<div
	class="canvas-container"
	tabindex="-1"
	on:focusin={handleCanvasFocus}
	on:focusout={handleCanvasBlur}
>
	<canvas
		bind:this={canvas}
		on:pointerdown={handlePointerDown}
		on:pointerup={handlePointerUp}
		on:pointermove={handlesCursor ? handlePointerMove : null}
		on:dblclick={handleDoubleClick}
		style="height: {height}; width: {width};"
		class="canvas-annotator"
	></canvas>
</div>

{#if interactive}
	<span class="canvas-control">
		<button
			class="icon"
			class:selected={mode === Mode.creationLine}
			aria-label="Create line"
			on:click={() => setCreateLineMode()}><Line/></button
		>
		<button
			class="icon"
			class:selected={mode === Mode.creation}
			aria-label="Create box"
			on:click={() => setCreateMode()}><BoundingBox/></button
		>
		<button
			class="icon"
			class:selected={mode === Mode.drag}
			aria-label="Edit boxes"
			on:click={() => setDragMode()}><Hand/></button
		>
		{#if showRemoveButton}
			<button
				class="icon"
				aria-label="Remove boxes"
				on:click={() => onDeleteBox()}><Trash/></button
			>
		{/if}
	</span>
{/if}

{#if editModalVisible}
	<ModalBox
		on:change={onModalEditChange}
		on:enter{onModalEditChange}
		choices={choices}
		choicesColors={choicesColors}
		name={selectedBox >= 0 && selectedBox < value.boxes.length ? value.boxes[selectedBox].name : ""}
		label={selectedBox >= 0 && selectedBox < value.boxes.length ? value.boxes[selectedBox].label : ""}
		color={selectedBox >= 0 && selectedBox < value.boxes.length ? colorRGBAToHex(value.boxes[selectedBox].color) : ""}
	/>
{/if}

{#if newModalVisible}
	<ModalBox
		on:change={onModalNewChange}
		on:enter{onModalNewChange}
		choices={choices}
		showRemove={false}
		choicesColors={choicesColors}
		label={selectedBox >= 0 && selectedBox < value.boxes.length ? value.boxes[selectedBox].label : ""}
		color={selectedBox >= 0 && selectedBox < value.boxes.length ? colorRGBAToHex(value.boxes[selectedBox].color) : ""}
	/>
{/if}

<style>
	.canvas-annotator {
		border-color: var(--block-border-color);
		width: 100%;
		height: 100%;
		display: block;
		touch-action: none;
	}

	.canvas-control {
		display: flex;
		align-items: center;
		justify-content: center;
		border-top: 1px solid var(--border-color-primary);
		width: 95%;
		bottom: 0;
		left: 0;
		right: 0;
		margin-left: auto;
		margin-right: auto;
		margin-top: var(--size-2);
	}

	.icon {
		width: 22px;
		height: 22px;
		margin: var(--spacing-lg) var(--spacing-xs);
		padding: var(--spacing-xs);
		color: var(--neutral-400);
		border-radius: var(--radius-md);
	}

	.icon:hover,
	.icon:focus {
		color: var(--color-accent);
	}
	
	.selected {
		color: var(--color-accent);
	}

	.canvas-container {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.canvas-container:focus {
    	outline: none;
	}
</style>
