// // src/components/Header.js
// import React, { useContext } from 'react';
// import { Link } from 'react-router-dom';
// import { AuthContext } from '../context/AuthContext';

// const Header = () => {
//   const { user } = useContext(AuthContext);

//   return (
//     <header className="header">
//       <nav className="nav-logged-in">
//         <ul>
//           <li><Link to="/">Home</Link></li>
//           <li><Link to="/connect">Friends</Link></li>
//           <li><Link to="/users">People</Link></li>
//           <li><Link to="/received-interests">Notifications</Link></li>
//           <li><Link to="/logout">Logout</Link></li>
//         </ul>
//       </nav>
//     </header>
//   );
// };

// export default Header;


// src/components/Header.js
import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Header = () => {
  const { user } = useContext(AuthContext);

  return (
    <header className="header">
      <div className="greeting">
        <p>Hello, {user ? user.username : 'Guest'}</p>
        <p>Stay Connected With Your Friends</p>
      </div>
      <nav className="nav-logged-in">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/connect">Friends</Link></li>
          <li><Link to="/users">People</Link></li>
          <li><Link to="/received-interests">Notifications</Link></li>
          <li><Link to="/logout">Logout</Link></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
