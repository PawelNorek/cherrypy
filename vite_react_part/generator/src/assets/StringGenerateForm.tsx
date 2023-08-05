import React from 'react'

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
	const handleCreate = (e: { preventDefault: () => void }) => {
		e.preventDefault()
		onCreateString()
	}

	const handleReplace = (e: { preventDefault: () => void }) => {
		e.preventDefault()
		onReplaceString()
	}

	const handleDelete = (e: { preventDefault: () => void }) => {
		e.preventDefault()
		onDeleteString()
	}

	const handleLengthChange = (e: { preventDefault: () => void; target: { value: string } }) => {
		e.preventDefault()
		const newLength = e.target.value.trim()
		onLengthChange(newLength)
	}

	const handleStringChange = (e: { preventDefault: () => void; target: { value: string } }) => {
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
