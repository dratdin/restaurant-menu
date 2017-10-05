import React from 'react'
import { Router, Route, Link } from "react-router-dom"
import createBrowserHistory from "history/createBrowserHistory"
import List from './List'
import Cart from './Cart'
import Form from './Form'

const history = createBrowserHistory();

class App extends React.Component {

    render() {
        return (
            <Router history={history}>
                <div className="container">
                    <div className="row no-gutters mt-3">
                        <div className="col-2">
                            <div className="list-group">
                                <Link to="/" className="list-group-item">My carts</Link>
                                <Link to="/new-cart" className="list-group-item">New cart</Link>
                                <a href="http://localhost:8000" className="list-group-item">&larr; to menu</a>
                            </div>
                        </div>

                        <main className="col-10" role="main">
                            <div className="pl-3">
                                <Route exact path="/" component={List} />
                                <Route exact path="/new-cart" 
                                component={props => <Form action="create" actionName="New cart" {...props} />} />
                                <Route exact path="/update-cart/:pk" 
                                component={props => <Form action="update" actionName="Update cart" {...props} />} />
                                <Route exact path="/detail/:pk" component={Cart} />
                            </div>
                        </main>
                    </div>
                </div>
            </Router>
        )
    }
}

export default App;