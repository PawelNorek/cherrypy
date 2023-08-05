import React from 'react'
import StringGeneratorForm from './StringGenerateForm'
import { useState } from 'react'

const StringGeneratorBox = () => {
	const [length, setLength] = useState('8')
	const [string, setString] = useState('')
	const [mode, setMode] = useState('create')

	const url = 'http://192.168.1.191:8099/generator'

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
				setLength(newString.length.toString())
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

	const handleLengthChange = (newLength: React.SetStateAction<string>) => {
		setLength(newLength)
		setString('')
		setMode('create')
	}

	const handleStringChange = (newString: React.SetStateAction<string>) => {
		setLength(newString.length.toString())
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

export default StringGeneratorBox
