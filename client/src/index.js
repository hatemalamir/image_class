import React from "react";
import Webcam from "react-webcam";
import ReactDOM from "react-dom";
import "./index.css";

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

  componentDidMount() {
    fetch("http://localhost:5000/api/v1.0/test")
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result.items,
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      );
  }

  render() {
    return (
      <>
        Hello
      </>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("root"));
