'use strict'

const e = React.createElement

function rIcon(filename) {
  return e('img', {src: `/icon/${filename}`, className: 'clickable', style: {filter: 'invert(1)'}, alt: filename, height: 24, width: 24})
}

const htmlFilename = window.location.pathname.slice(6)
const filename = decodeURIComponent(htmlFilename)

class IndexPage extends React.Component {
  render() {
    return e('div', {id: 'indexPage'},
      e(Navbar),
      e('div', {id: 'placeholder', style: {marginTop: '20px'}}),
    )
  }
}

class Navbar extends React.Component {
  constructor(props) {
    super(props)
    this.state = {showActionDropdown: false, marginWidth: '15%'}
  }

  render() {
    const {showActionDropdown, marginWidth} = this.state
   
    return e('div', {className: 'navbar'},
      e('a', {href: 'http://localhost:3000/'}, 'Acceuil'), // Home is a link where there are links to all else
      e('a', {href: 'http://localhost:3000/'}, 'Repas'),
      e('a', {href: 'http://localhost:3000/'}, 'Dessert'),
      e('input', {id: 'filterVal2', onKeyDown: this.onKeyDown, type: 'text', value: this.state.query, onChange: ({target}) => {this.setState({query: target.value})}}),
      e('a', {href: 'http://localhost:3000/'}, 'À propos'),
      //e('a', {href: `http://localhost:3000/edit/${encodeURIComponent(filename)}`}, 'Edit'),
      e('span', {className: 'dropdown'},
        e('button', {className: 'dropbtn', onClick: () => {this.setState({showActionDropdown: !showActionDropdown})}}, 'Ingrédients', e('i', {className: 'fa fa-caret-down'})),
        showActionDropdown ? e('div', {id: 'myDropdown', className: 'dropdown-content'},
          e('div', null, 'Show 1'),
          e('div', null, 'Show 2'),
        ) : null,
      ),
      e('span', {onClick: () => {
        if (marginWidth === '0%') {
          $('#root').css('margin-left', '15%')
          $('#root').css('margin-right', '15%')
          this.setState({marginWidth: '15%'})
        } else if (marginWidth === '15%') {
          $('#root').css('margin-left', '0%')
          $('#root').css('margin-right', '0%')
          this.setState({marginWidth: '0%'})
        }
      }}, rIcon('aspect_ratio-24px.svg')),
    )
  }
}

ReactDOM.render(e(IndexPage), document.querySelector('#root'));

$(document).ready(function() {
  //$('#placeholder').load('/data/relish.html');
  $('#placeholder').load(encodeURIComponent('data/Crêpe hollandaise #déjeuner #recette'));
  //$('#placeholder').load(encodeURIComponent('data/a test.html'));
});
