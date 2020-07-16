import React from 'react';
import ImageUploader from 'react-images-upload';
import {useDropzone} from 'react-dropzone'

class ImageUpload extends React.Component {

    constructor(props) {
        super(props);
         this.state = { pictures: [] };
         this.onDrop = this.onDrop.bind(this);
    }

    onDrop(picture) {
        this.setState({
            pictures: this.state.pictures.concat(picture),
        });
    }



    render() {
console.log(this.state)
        return (
            <ImageUploader
                withIcon={true}
                buttonText='Choose images'
                onChange={this.onDrop}
                imgExtension={['.jpg', '.gif', '.png', '.gif','.mkv','.mp4']}
                maxFileSize={52428800}
            />
        );
    }
}

export default ImageUpload
