import { useState } from 'react'

const StringGeneratorBox = () => {
	const [length, setLength] = useState('8')
	const [string, setString] = useState('')
	const [mode, setMode] = useState('create')

	const url = '/generator'

	const handleGenerate = () => {
		let formdata = new FormData()
		formdata.append('length', length)

		fetch(url, {
			method: 'POST',
			body: formdata,
		})
			.then(response => response.text())
			.then(data => {
				setLength(length)
				setString(data)
				setMode('edit')
			})
			.catch(error => {
				console.error('/generator', error)
			})
	}

	const handleEdit = () => {
		const newString = string
		let formdata = new FormData()
		formdata.append('another_string', newString)
		fetch(url, {
			method: 'PUT',
			body: formdata,
		})
			.then(() => {
				setLength(newString.length)
				setString(newString)
				setMode('edit')
			})
			.catch(error => {
				console.error('/generator', error)
			})
	}

	const handleDelete = () => {
		fetch(url, {
			method: 'DELETE',
		})
			.then(() => {
				setLength('8')
				setString('')
				setMode('create')
			})
			.catch(error => {
				console.error('/generator', error)
			})
	}

	const handleLengthChange = newLength => {
		setLength(newLength)
		setString('')
		setMode('create')
	}

	const handleStringChange = newString => {
		setLength(newString.length)
		setString(newString)
		setMode('edit')
	}

	return (
		<div className='stringGenBox'>
			<StringGeneratorForm
				onCreateString={handleGenerate}
				onReplaceString={handleEdit}
				onDeleteString={handleDelete}
				onLengthChange={handleLengthChange}
				onStringChange={handleStringChange}
				mode={mode}
				length={length}
				string={string}
			/>
		</div>
	)
}

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

const App = () => {
	return <StringGeneratorBox />
}

export default App
