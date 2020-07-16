import React, {useCallback,useState,useEffect} from 'react'
import { Slide } from 'react-slideshow-image';
import axios from 'axios'
import {useDropzone} from 'react-dropzone'
import SVGUpload from '../SVGUpload'
import MonkeyCard from '../MonkeyCard'

import "./Upload.scss"

import 'react-slideshow-image/dist/styles.css'

export default function Upload() {
  const [images, setImages]= useState([])
  const [loading, setLoading]= useState(false)
  const [classImg,setClassImg] = useState([])

  const onClassifier = () =>{
    images.map((obj)=>{
        console.log(obj)
    })
  }

  const onDrop = useCallback((acceptedFiles) => {
    const filesURL = []
    setLoading(true)
    let data = new FormData();
    console.log(acceptedFiles)

    // for (var i = 0; i < acceptedFiles.length; i++) {
    //         let file = files.item(i);
    //         data.append('images[' + i + ']', file, file.name);
    // }
    acceptedFiles.map((file) => {
      const reader = new FileReader()

      reader.onabort = () => console.log('file reading was aborted')
      reader.onerror = () => console.log('file reading has failed')

      reader.onload = async () => {
      // Do whatever you want with the file contents
        const urlFi = reader.result
        const classifiedImg = []
        const rsult = await axios.post('http://localhost:5000/api/class',{"url": urlFi,"name":file.name })
        console.log(classifiedImg)
        console.log(rsult)
        const classImg = "data:image/jpeg;base64," + rsult.data
        filesURL.push({"original":urlFi, "file":file,"classified":classImg,"label":"test"})
        // setImages(filesURL)
      }
      //console.log(file)
      //reader.readAsArrayBuffer(file)
      reader.readAsDataURL(file)
    })

    setImages(filesURL)
    setLoading(false)
  }, [])

useEffect(()=>{
if(images.length == 0){
  setLoading(true)
}else{
  setLoading(false)
}

},[images])

  const {getRootProps, getInputProps} = useDropzone({onDrop})

console.log(images)
  return (
    <>
    <div className="Upload" {...getRootProps()}>
      <SVGUpload />
      <input {...getInputProps()} />
      <p>Drag 'n' drop some files here, or click to select files</p>
    </div>
    {loading && <p>LOADING</p>}
    {images.length > 0 && (<Slide>{images.map((src)=>(<div className="Upload_slide"><div><img src={src.original}/></div><div><img src={src.classified}/></div></div>))}</Slide>)}

    </>
  )
}
