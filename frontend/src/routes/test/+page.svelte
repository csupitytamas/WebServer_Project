<script lang="ts">
	import FormGeneratorv2 from '$lib/components/FormGeneratorv2.svelte';
</script>

<FormGeneratorv2
	title="Test Form"
	inputs={[
		{ label: 'Name', placeholder: 'Enter your name', value: '' },
		{ label: 'Email', placeholder: 'Enter your email', value: '' }
	]}
	data={[[{ value: 'John Doe' }, { value: 'asd' }], [{ value: 'asd' }], [{ value: '123' }]]}
/>
