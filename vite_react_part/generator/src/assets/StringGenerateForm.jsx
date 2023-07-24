const StringGeneratorForm = ({
	onCreateString,
	onReplaceString,
	onDeleteString,
	onLengthChange,
	onStringChange,
	mode,
	length,
	string,
}) => {
	const handleCreate = e => {
		e.preventDefault()
		onCreateString()
	}

	const handleReplace = e => {
		e.preventDefault()
		onReplaceString()
	}

	const handleDelete = e => {
		e.preventDefault()
		onDeleteString()
	}

	const handleLengthChange = e => {
		e.preventDefault()
		const newLength = e.target.value.trim()
		onLengthChange(newLength)
	}

	const handleStringChange = e => {
		e.preventDefault()
		const newString = e.target.value.trim()
		onStringChange(newString)
	}

	if (mode === 'create') {
		return (
			<div>
				<input type='text' value={length} onChange={handleLengthChange} />
				<button onClick={handleCreate}>Give it now!</button>
			</div>
		)
	} else if (mode === 'edit') {
		return (
			<div>
				<input type='text' value={string} onChange={handleStringChange} />
				<button onClick={handleReplace}>Replace</button>
				<button onClick={handleDelete}>Delete it</button>
			</div>
		)
	}

	return null
}

export default StringGeneratorForm
