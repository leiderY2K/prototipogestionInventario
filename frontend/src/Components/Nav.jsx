import * as React from 'react';
import PropTypes from 'prop-types';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import MenuIcon from '@mui/icons-material/Menu';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { Link, useLocation } from "react-router-dom";  // Removed Outlet
import HomeIcon from '@mui/icons-material/Home';
import BarChartIcon from "@mui/icons-material/BarChart";
import PeopleIcon from "@mui/icons-material/People";
import StoreIcon from "@mui/icons-material/Store"
import ScienceIcon from "@mui/icons-material/Science";
import imgs from "/src/img/imgs.js";
import CardMedia from '@mui/material/CardMedia';

const drawerWidth = 240;

function Nav(props) {
  const { window } = props;
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const location = useLocation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <Box sx={{ backgroundColor: '#8c1919', height: '100%', color: '#fff' }}>
      <Box sx={{
        backgroundColor: '#8c1919',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        p: 0.2,
        gap: 2.5,
        flexDirection: 'row',
      }}>
        <CardMedia
          component="img"
          image={imgs[0]}
          alt="Logo Universidad"
          sx={{
            width: 'auto',
            maxHeight: 60,
          }}
        />
        <CardMedia
          component="img"
          image={imgs[1]}
          alt="Logo Virtus"
          sx={{
            width: 'auto',
            maxHeight: 60,
          }}
        />
      </Box>
      <Divider sx={{ backgroundColor: '#8c1919' }} />
      <List>
        {[
          { text: 'Inicio', icon: <HomeIcon />, route: '/' },
          { text: 'Productos', icon: <StoreIcon />, route: '/products' },
          { text: 'Estadísticas', icon: <BarChartIcon />, route: '/statistics' },
          { text: 'Usuarios', icon: <PeopleIcon />, route: '/users' },
          { text: 'Investigadores', icon: <ScienceIcon />, route: '/researchers' },
        ].map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              component={Link}
              to={item.route}
              sx={{
                '&:hover': {
                  backgroundColor: '#fff',
                  '& .MuiListItemIcon-root': {
                    color: '#8c1919',
                  },
                  '& .MuiTypography-root': {
                    color: '#8c1919',
                  },
                },
              }}
            >
              <ListItemIcon sx={{ color: '#fff' }}>{item.icon}</ListItemIcon>
              <ListItemText
                primary={item.text}
                sx={{
                  color: '#fff',
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          backgroundColor: '#8c1919',
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Repositorio Virtus
          </Typography>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="mailbox folders"
      >
        <Drawer
          container={window ? window().document.body : undefined}
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}
      >
        <Toolbar />
        {props.children}
      </Box>
    </Box>
  );
}

Nav.propTypes = {
  window: PropTypes.func,
  children: PropTypes.node
};

export default Nav;