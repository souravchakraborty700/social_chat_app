// // src/components/Home.js
// import React, { useContext } from 'react';
// import { Link } from 'react-router-dom';
// import { AuthContext } from '../context/AuthContext';
// import Header from './Header';

// const Home = () => {
//   const { user, loading } = useContext(AuthContext);

//   if (loading) {
//     return <div>Loading...</div>;
//   }

//   return (
//     <div className="home-container">
//       {user ? (
//         <>
//           <Header />
//           <div className="welcome">
//             <h1>Welcome to Social Chat</h1>
//             <p>Explore and connect with friends</p>
//           </div>
//         </>
//       ) : (
//         <>
//           <h1>Social Chat</h1>
//           <h2>Let's connect...</h2>
//           <nav>
//             <ul>
//               <li><Link to="/login">Login</Link></li>
//               <li><Link to="/register">Register</Link></li>
//             </ul>
//           </nav>
//         </>
//       )}
//     </div>
//   );
// };

// export default Home;


// src/components/Home.js
import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import Header from './Header';

const Home = () => {
  const { user, loading } = useContext(AuthContext);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="home-container">
      {user ? (
        <>
          <Header />
          <div className="welcome">
            <h1>Welcome to Social Chat</h1>
            <p>Explore and connect with friends</p>
          </div>
        </>
      ) : (
        <>
          <h1>Social Chat</h1>
          <h2>Let's connect...</h2>
          <nav>
            <ul>
              <li><Link to="/login">Login</Link></li>
              <li><Link to="/register">Register</Link></li>
            </ul>
          </nav>
        </>
      )}
    </div>
  );
};

export default Home;
