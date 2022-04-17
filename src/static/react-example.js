const e = React.createElement;

class ClickCounter extends React.Component {
  constructor(props) {
    super(props);
    this.state = { clickCount: 0 };
  }

  render() {
    return e("button", {
      onclick: () => this.setState({ clickCount: this.state.clickCount + 1 }),
    });
  }
}
