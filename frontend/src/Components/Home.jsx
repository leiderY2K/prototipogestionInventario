import { Box, Card, CardContent, CardMedia, Typography, Grid } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import BarChartIcon from "@mui/icons-material/BarChart";
import PeopleIcon from "@mui/icons-material/People";
import ScienceIcon from "@mui/icons-material/Science";
import StoreIcon from "@mui/icons-material/Store"

const Home = () => {
  const navigate = useNavigate();

  const cards = [
    {
        title: 'Productos',
        description: 'Explora información sobre productos',
        icon: <StoreIcon sx={{ fontSize: 60, color: '#8c1919' }} />,
        route: '/products'
    },
    {
        title: 'Estadísticas',
        description: 'Visualiza estadísticas y métricas importantes',
        icon: <BarChartIcon sx={{ fontSize: 60, color: '#8c1919' }} />,
        route: '/statistics'
    },
    {
        title: 'Usuarios',
        description: 'Gestiona los usuarios del sistema',
        icon: <PeopleIcon sx={{ fontSize: 60, color: '#8c1919' }} />,
        route: '/users'
    },
    {
        title: 'Investigadores',
        description: 'Explora información sobre investigadores',
        icon: <ScienceIcon sx={{ fontSize: 60, color: '#8c1919' }} />,
        route: '/researchers'
    }
  ];

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom sx={{ color: '#8c1919', mb: 4 }}>
        Bienvenido al Repositorio Virtus
      </Typography>

      <Typography variant="body1" component="p" sx={{ fontSize: '0.875rem', color: '#000', mb: 2 }}>
        En este aplicativo podrás visualizar en tiempo real los productos existentes, filtrar por tipo de producto, investigador, años, entre otros, y también podrás visualizar el producto.
        </Typography>
      
      <Grid container spacing={4}>
        {cards.map((card) => (
          <Grid item xs={12} sm={6} md={4} key={card.title}>
            <Card 
              sx={{ 
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                cursor: 'pointer',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-5px)',
                  boxShadow: '0 8px 16px rgba(140, 25, 25, 0.2)',
                },
                border: '1px solid #e0e0e0'
              }}
              onClick={() => navigate(card.route)}
            >
              <Box
                sx={{
                  p: 3,
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  backgroundColor: '#f5f5f5'
                }}
              >
                {card.icon}
              </Box>
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h5" component="h2" sx={{ color: '#8c1919' }}>
                  {card.title}
                </Typography>
                <Typography>
                  {card.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Home;