import React from 'react'

import DeleteImg from './img/trash.png'
import EditImg from './img/pencil.png'

import { Link } from "react-router-dom"
import ajaxSetup from './ajaxSetup'

class List extends React.Component {
    state = {
        carts: [],
        currentCartPk: null
    };

    loadCarts() {
        window.$.ajax({
            method: 'GET',
            url: '/api/carts/',
            success: (data) => {
                this.setState({
                    carts: data['carts'],
                    currentCartPk: data['current_cart_pk']
                })
            },
            error: () => {
                console.error('Carts loading was failed');
            }
        });
    }

    setCurrentCart(pk) {
        window.$.ajax({
            method: 'GET',
            url: `/api/carts/set-as-current/${pk}`,
            success: (data) => {
                this.setState({
                    currentCartPk: data['current_cart_pk']
                })
            },
            error: (xhr, status, error) => {
                alert(xhr.responseText);
                console.error('Cant set cart as current');
            }
        });
    }

    deleteCart(pk) {
        ajaxSetup();
        window.$.ajax({
            method: 'DELETE',
            url: `/api/carts/delete/${pk}`,
            success: (data) => {
                this.setState({
                    carts: data['carts'],
                    currentCartPk: data['current_cart_pk']
                })
            },
            error: (xhr, status, error) => {
                alert(xhr.responseText);
                console.error('Cart deleting was failed');
            }
        });
    }

    componentDidMount() {
        this.loadCarts();
    }

    cartButtons(cart) {
        // return React.createElement(CustomButton, {color: 'red'}, null);
        return (
            <td className="actions">
                <div className="btn btn-success mr-1" 
                onClick={() => this.setCurrentCart(cart['pk'])}
                style={{ cursor: 'pointer'}}>Set as current</div>
                <Link to={`/update-cart/${cart['pk']}`} className="btn btn-primary mr-1"><img src={EditImg} alt="edit"/></Link>
                <div className="btn btn-danger" 
                style={{ cursor: 'pointer'}}
                onClick={() => this.deleteCart(cart['pk'])} >
                    <img src={DeleteImg} alt="delete"/>
                </div>
            </td>
        );
    }

    currentCartButtons(cart) {
        // return React.createElement(CustomButton, {color: 'red'}, null);
        return (
            <td className="actions">
                <button type="button" className="btn btn-secondary" disabled>Set as current</button>
                <Link to={`/update-cart/${cart['pk']}`} className="btn btn-primary mr-1"><img src={EditImg} alt="edit"/></Link>
                <button className="btn btn-secondary" disabled >
                    <img src={DeleteImg} alt="delete"/>
                </button>
            </td>
        );
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
                            <Link to={`/detail/${cart.pk}`}>
                                <h5 className="nomargin">{ cart['name'] }</h5>
                            </Link>
                            <p>{ cart['description'] }</p>
                        </td>
                        <td data-th="Items">{ cart['count'] }</td>
                        <td data-th="Total price">${ cart['summary'] }</td>
                            {
                                cart["pk"] !== this.state.currentCartPk ? this.cartButtons(cart) :
                                    this.currentCartButtons(cart)
                            }
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        );
    }
}

export default List