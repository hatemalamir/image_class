import React from "react";
import Webcam from "react-webcam";
import ReactDOM from "react-dom";
import MonkeyCard from "./components/MonkeyCard"
import ImageUpload from "./components/uploads/ImageUpload"
import Upload from "./components/uploads/Upload"
import "./index.scss";


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: [],
    };
  }

  WebcamComponent = () => <Webcam />;

  componentDidMount() {}

  render() {
    return (
      <div className="App">
        <Upload  />
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("root"));
