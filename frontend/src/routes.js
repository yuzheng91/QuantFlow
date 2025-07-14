import React from 'react';

import { Icon } from '@chakra-ui/react';
import {
  MdArticle,
  MdPerson,
  MdHome,
  MdLock,
  MdOutlineShoppingCart,
} from 'react-icons/md';
import { AiOutlineStock } from "react-icons/ai";

// Admin Imports
import MainDashboard from 'views/admin/default';
import CustomStrategy from 'views/admin/CustomStrategy';
import Blog from 'views/admin/blog';
import NFTMarketplace from 'views/admin/marketplace';
import Profile from 'views/admin/profile';

// Auth Imports
import SignInCentered from 'views/auth/signIn';

const routes = [
  {
    name: 'Main Dashboard',
    layout: '/admin',
    path: '/default',
    icon: <Icon as={MdHome} width="20px" height="20px" color="inherit" />,
    component: <MainDashboard />,
  },
  {
    name: 'Custom Strategy',
    layout: '/admin',
    path: '/CustomStrategy',
    icon: <Icon as={AiOutlineStock} width='20px' height='20px' color='inherit' />,
    component: <CustomStrategy />,
  },
  {
    name: 'Blog',
    layout: '/admin',
    path: '/blog',
    icon: <Icon as={MdArticle} width='20px' height='20px' color='inherit' />,
    component: <Blog />,
  },
  {
    name: 'NFT Marketplace',
    layout: '/admin',
    path: '/nft-marketplace',
    icon: (
      <Icon
        as={MdOutlineShoppingCart}
        width="20px"
        height="20px"
        color="inherit"
      />
    ),
    component: <NFTMarketplace />,
    secondary: true,
  },
  {
    name: 'Profile',
    layout: '/admin',
    path: '/profile',
    icon: <Icon as={MdPerson} width="20px" height="20px" color="inherit" />,
    component: <Profile />,
  },
  {
    name: 'Sign In',
    layout: '/auth',
    path: '/sign-in',
    icon: <Icon as={MdLock} width="20px" height="20px" color="inherit" />,
    component: <SignInCentered />,
  },
];

export default routes;
