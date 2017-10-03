import React from 'react'


class Cart extends React.Component {
    state = {
        cart: {
            item_set: []
        }
    };

    loadCart() {
        let url = "/api/carts/" + this.props.match.params.pk
        window.$.ajax({
            method: 'GET',
            url: url,
            success: (data) => {
                this.setState({cart: data})
            },
            error: () => {
                console.error('Cart loading was failed');
            }
        });
    }

    removeFromCart(item) {
        let url = `/api/carts/remove-from-cart/${this.state.cart.pk}/${item.dish.id}/`;
        console.log(url);
        window.$.ajax({
            url: url,
            type: 'GET',
            data: {},
            success: (data) => {
                this.setState({ cart: data });
            },
            error: () => console.error('Cart loading was failed')
        });
    }

    componentDidMount() {
        this.loadCart();
    }

    render() {
        return (
            <div className="pl-3">
                <h1>{ this.state.cart['name'] }</h1>

                <table id="cart" className="table table-hover table-condensed border">
                <thead>
                    <tr>
                    <th styles={{width:'50%'}}>Product</th>
                    <th styles={{width:'10%'}}>Price</th>
                    <th styles={{width:'10%'}}>Quantity</th>
                    <th styles={{width:'15%'}} className="text-center">Subtotal</th>
                    <th styles={{width:'15%'}}></th>
                    </tr>
                </thead>
                <tbody>
                    { this.state.cart['item_set'].map((item, index)=>(
                    <tr className="product" key={index}>
                    <td>
                        <h5 className="nomargin">{ item.dish.name }</h5>
                    </td>
                    <td data-th="Price">${ item.unit_price }</td>
                    <td data-th="Quantity">{ item.quantity }</td>
                    <td data-th="Subtotal" className="text-center">${ item.total_price }</td>
                    <td className="actions" data-th="">
                        <button onClick={() => this.removeFromCart(item)}
                         className="btn btn-danger btn-sm product-remove">Remove</button>
                    </td>
                    </tr>
                    ))}
                </tbody>
                <tfoot>
                    <tr>
                    <td colSpan="3" className="hidden-xs"></td>
                    <td className="hidden-xs text-center">
                        <strong>
                            Total $
                            <span className="cart__sum">{ this.state.cart.summary }</span>
                        </strong>
                        </td>
                    <td colSpan="1" className="hidden-xs"></td>
                    </tr>
                </tfoot>
                </table>
            </div>
        )
    }
}


export default Cart