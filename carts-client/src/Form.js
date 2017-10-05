import React from 'react'
import { Redirect } from 'react-router-dom'
import ajaxSetup from './ajaxSetup'

class Form extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            completed: false,
            name: '',
            description: ''
        }

        if(props.action === "create") {
            this.handleSubmit = this.createCart.bind(this);
        } else if(props.action === "update") {
            this.handleSubmit = this.updateCart.bind(this);
        } else if(props.action == null){
            console.error("props.action is undefined");
        } else {
            console.error("Unknown props.action");
        }
    }
  
    createCart(event) {
        event.preventDefault();

        let url = "/api/carts/create/";
        let data = {
            name: this.state.name, 
            description: this.state.description
        };
        ajaxSetup();
        window.$.ajax({
            method: 'POST',
            url: url,
            data: data,
            success: (data) => {
                this.setState({completed: true})
            },
            error: (xhr, status, error) => {
                alert(xhr.responseText);
                console.error('Cart creating was failed');
                console.log(data);
            }
        });
    }

    updateCart(event) {
        event.preventDefault();

        let url = `/api/carts/update/${this.props.match.params.pk}/`;
        console.log(url);
        let data = {
            name: this.state.name, 
            description: this.state.description
        };
        ajaxSetup();
        window.$.ajax({
            method: 'PUT',
            url: url,
            data: data,
            success: (data) => {
                this.setState({completed: true})
            },
            error: (xhr, status, error) => {
                alert(xhr.responseText);
                console.error('Cart updating was failed');
                console.log(data);
            }
        });
    }

    loadCart() {
        let url = `/api/carts/update/${this.props.match.params.pk}/`;
        window.$.ajax({
            method: 'GET',
            url: url,
            success: (data) => {
                this.setState({
                    name: data.name,
                    description: data.description
                })
            },
            error: (xhr, status, error) => {
                console.error('Cart loading was failed!');
            }
        });
    }

    componentDidMount() {
        if(this.props.action === "update")
            this.loadCart();
    }
  
    render() {
        if(this.state.completed === true)
            return (<Redirect to="/" />)
        else
            return (
                <div>
                    <h1>{this.props.actionName}</h1>
                    <form onSubmit={ this.handleSubmit }>
                        <div className="form-group">
                            <input 
                            type="text" 
                            placeholder="Name" 
                            value={this.state.name} 
                            onChange={e => this.setState({name: e.target.value})} />
                        </div>
                        <div className="form-group">
                            <textarea 
                            placeholder="Description" 
                            value={this.state.description} 
                            onChange={e => this.setState({description: e.target.value})} />
                        </div>
                        <input type="submit" className="btn btn-primary" value="Submit" />
                    </form>
                </div>
            );
    }
  }


export default Form