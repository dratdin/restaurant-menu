import React from 'react'

class ListItem extends React.Component {
    render() {
      return (
        <div>
          <h2>{this.props.cart.name}</h2>
          <div>{this.props.cart.description}</div>
        </div>
      );
    }
  }

export default ListItem