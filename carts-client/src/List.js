import React from 'react'
import ListItem from './ListItem'

import DeleteImg from './img/trash.png'
import EditImg from './img/pencil.png'

class List extends React.Component {
    state = {
        carts: []
    };

    loadCarts() {
        window.$.ajax({
            method: 'GET',
            url: 'http://localhost:8000/api/carts/',
            success: (data) => {
                this.setState({carts: data})
            },
            error: () => {
                console.error('Cart loading was failed');
            }
        });
    }

    componentDidMount() {
        this.loadCarts();
    }

    render(){
        return(
            <div className="pl-3">
                <h1>My Carts</h1>
                <table id="cart" className="table table-hover table-condensed border">
                    <thead>
                        <tr>
                        <th styles={{width:'40%'}}>Cart</th>
                        <th styles={{width:'10%'}}>Items</th>
                        <th styles={{width:'15%'}}>Total price</th>
                        <th styles={{width:'35%'}}>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                    {this.state.carts.map((cart, index) => (
                        <tr className="product" key={index}>
                        <td>
                            <h5 className="nomargin">{ cart['name'] }</h5>
                            <p>{ cart['description'] }</p>
                        </td>
                        <td data-th="Items">{ cart['count'] }</td>
                        <td data-th="Total price">${ cart['summary'] }</td>
                        <td className="actions">
                            <div className="btn btn-success mr-1">Set as current</div>
                            <div className="btn btn-primary mr-1"><img src={EditImg} alt="edit"/></div>
                            <div className="btn btn-danger"><img src={DeleteImg} alt="delete"/></div>
                        </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        );
    }
}

export default List