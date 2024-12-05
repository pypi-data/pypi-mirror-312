<svelte:options immutable={true} />

<script lang="ts">
	import type { Gradio, SelectData } from "@gradio/utils";
	import { Block, BlockTitle } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { createEventDispatcher } from "svelte";

	const dispatch = createEventDispatcher();

	export let gradio: Gradio<{
		change: never;
		select: SelectData;
		input: never;
	}>;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: (string | number)[] = [];
	export let choices: [string, string | number][];
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let label = gradio.i18n("checkbox.checkbox_group");
	export let info: string | undefined = undefined;
	export let show_label = true;

	export let loading_status: LoadingStatus;
	export let interactive = true;
	export let old_value = value.slice();
	export let is_collapsed = false;

	let count_selected_val = 0;

	function toggle_choice(choice: string | number): void {
		if (value.includes(choice)) {
			value = value.filter((v) => v !== choice);
		} else {
			value = [...value, choice];
		}
		dispatch("input", value);
	}

	function select_all(): void {
		choices.forEach((v, i) => {
			const [_, internal_value] = v;
			if (!value.includes(internal_value)) {
				value = [...value, internal_value];
			}
			gradio.dispatch("select", {
				index: i,
				value: internal_value,
				selected: true,
			});
		});
		dispatch("input", value);
	}

	function select_none(): void {
		choices.forEach((c, i) => {
			const [_, internal_value] = c;
			value = value.filter((v) => v != internal_value);
			gradio.dispatch("select", {
				index: i,
				value: internal_value,
				selected: false,
			});
		});
	}

	function count_selected(c, val): number {
		if (!c) {
			return 0;
		}
		const r = c.filter((v) => {
			const [_, internal_value] = v;
			return val.includes(internal_value);
		});
		return r.length;
	}

	function collapse() {
		is_collapsed = !is_collapsed;
	}

	function group_choices(choices) {
		const groupped_choices = {};
		choices.forEach(([display_value, internal_value]) => {
			const [prefix, ...rest] = internal_value.split("_");
			if (!groupped_choices[prefix]) {
				groupped_choices[prefix] = [];
			}
			groupped_choices[prefix].push([
				rest.join("_") ?? internal_value,
				internal_value,
			]);
		});
		return groupped_choices;
	}

	let groupped_choices = {};

	$: groupped_choices = group_choices(choices);

	$: count_selected_val = count_selected(choices, value);

	$: disabled = !interactive;

	$: if (JSON.stringify(old_value) !== JSON.stringify(value)) {
		old_value = value;
		dispatch("change", value);
	}
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	type="fieldset"
	{container}
	{scale}
	{min_width}
>
	<StatusTracker
		autoscroll={gradio.autoscroll}
		i18n={gradio.i18n}
		{...loading_status}
	/>
	<div class="title">
		<div class="label">{label}</div>
		<div class="count">({count_selected_val}/{choices.length})</div>
		<div class="left">
			<button on:click={select_all} class="span-like-button">
				All
			</button>
			|
			<button on:click={select_none} class="span-like-button">
				None
			</button>
		</div>
		<span
			class="arrow"
			title="Click to collapse/expand"
			tabindex="0"
			on:click={collapse}
			on:keydown={(event) => {
				if (event.key === "Enter" || event.key === " ") {
					collapse();
				}
			}}
			role="button"
		>
			{#if is_collapsed}
				&#x25B6;
			{:else}
				&#x25BC;
			{/if}
		</span>
	</div>

	<div
		class="wrap"
		data-testid="checkbox-group"
		style={is_collapsed ? "display: none" : ""}
	>
		{#each Object.entries(groupped_choices) as [label, vals]}
			<div>
				<span><strong>{label}</strong></span>
				{#each vals as [display_value, internal_value], i}
					<label
						class:disabled
						class:selected={value.includes(internal_value)}
					>
						<input
							{disabled}
							on:change={() => toggle_choice(internal_value)}
							on:input={(evt) =>
								gradio.dispatch("select", {
									index: i,
									value: internal_value,
									selected: evt.currentTarget.checked,
								})}
							on:keydown={(event) => {
								if (event.key === "Enter") {
									toggle_choice(internal_value);
									gradio.dispatch("select", {
										index: i,
										value: internal_value,
										selected:
											!value.includes(internal_value),
									});
								}
							}}
							checked={value.includes(internal_value)}
							type="checkbox"
							name={internal_value?.toString()}
							title={internal_value?.toString()}
						/>
						<span class="ml-2">{display_value}</span>
					</label>
				{/each}
			</div>
		{/each}
	</div>
</Block>

<style>
	.wrap {
		display: flex;
		flex-wrap: wrap;
		gap: var(--checkbox-label-gap);
	}
	label {
		display: flex;
		align-items: center;
		transition: var(--button-transition);
		cursor: pointer;
		border-radius: var(--button-small-radius);
		background: var(--checkbox-label-background-fill);
		color: var(--checkbox-label-text-color);
		font-weight: var(--checkbox-label-text-weight);
		font-size: var(--checkbox-label-text-size);
		line-height: var(--line-md);
	}

	label:hover {
		background: var(--checkbox-label-background-fill-hover);
	}
	label:focus {
		background: var(--checkbox-label-background-fill-focus);
	}
	label.selected {
		background: var(--checkbox-label-background-fill-selected);
		color: var(--checkbox-label-text-color-selected);
	}

	label > * + * {
		margin-left: var(--size-2);
	}

	input {
		--ring-color: transparent;
		position: relative;
		box-shadow: var(--checkbox-shadow);
		border-radius: var(--checkbox-border-radius);
		background-color: var(--checkbox-background-color);
		line-height: var(--line-sm);
	}

	input:checked,
	input:checked:hover,
	input:checked:focus {
		border-color: var(--checkbox-border-color-selected);
		background-image: var(--checkbox-check);
		background-color: var(--checkbox-background-color-selected);
	}

	input:checked:focus {
		border-color: var(--checkbox-border-color-focus);
		background-image: var(--checkbox-check);
		background-color: var(--checkbox-background-color-selected);
	}

	input:hover {
		border-color: var(--checkbox-border-color-hover);
		background-color: var(--checkbox-background-color-hover);
	}

	input:not(:checked):focus {
		border-color: var(--checkbox-border-color-focus);
	}

	input[disabled],
	.disabled {
		cursor: not-allowed;
	}

	.title {
		display: grid;
		grid-template-columns: 13ex 5em auto auto;
		grid-auto-rows: min-content;
		position: relative;
		z-index: var(--layer-4);
		border: solid var(--block-title-border-width)
			var(--block-title-border-color);
		border-radius: var(--block-title-radius);
		background: var(--block-title-background-fill);
		padding: var(--block-title-padding);
		color: var(--block-title-text-color);
		font-weight: var(--block-title-text-weight);
		font-size: var(--block-title-text-size);
		line-height: var(--line-sm);
		margin-bottom: var(--spacing-lg);
	}

	.title .arrow {
		cursor: pointer;
		display: inline-block;
		margin-left: 5px;
		text-align: right;
	}
	.title .left {
		text-align: center;
	}
</style>
