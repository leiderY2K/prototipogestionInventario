import React, { useState, useEffect } from 'react';
import { Search, Filter, Download } from 'lucide-react';
import { Box, AppBar, Toolbar, Typography, Select, MenuItem, FormControl, InputLabel, CircularProgress, Card, CardContent } from '@mui/material';

const Products = () => {
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedType, setSelectedType] = useState("");
    const [productsData, setProductsData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Llamada a la API para cargar los productos
        fetch("http://localhost:5000/productos")
            .then((response) => response.json())
            .then((data) => {
                setProductsData(data);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error al cargar los productos:", error);
                setLoading(false);
            });
    }, []);

    const types = productsData.length > 0 
        ? [...new Set(productsData.map(product => product.idTipoDeProducto))]
        : [];
    
    const filteredProducts = productsData.filter(product => {
        const matchesSearch = product.TituloProducto.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesType = selectedType === "" || product.idTipoDeProducto === selectedType;
        return matchesSearch && matchesType;
    });

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#e9eaed' }}>
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', p: 3, backgroundColor: '#e9eaed' }}>
            {/* App Bar */}
            <AppBar position="fixed" sx={{ backgroundColor: '#8c1919', zIndex: 1201 }}>
                <Toolbar>
                    <Typography variant="h6" sx={{ flexGrow: 1 }}>
                        Productos de Investigación
                    </Typography>
                </Toolbar>
            </AppBar>

            {/* Main Content */}
            <Box sx={{ mt: 8 }}>
                {/* Filters and Search */}
                <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
                    <Box sx={{ flexGrow: 1 }}>
                        <Box sx={{ position: 'relative' }}>
                            <Search sx={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: 'gray' }} />
                            <input
                                type="text"
                                placeholder="Buscar por título..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                style={{
                                    width: '100%',
                                    paddingLeft: '40px',
                                    paddingRight: '16px',
                                    padding: '8px',
                                    backgroundColor: '#8c1919',
                                    color: 'white',
                                    borderRadius: '8px',
                                    border: '1px solid #444',
                                    transition: 'all 0.3s ease',
                                }}
                                onMouseEnter={(e) => e.target.style.borderColor = '#fff'}
                                onMouseLeave={(e) => e.target.style.borderColor = '#444'}
                            />
                        </Box>
                    </Box>

                    <FormControl sx={{ minWidth: 150 }} variant="outlined">
                        <InputLabel>Tipo de Producto</InputLabel>
                        <Select
                            value={selectedType}
                            onChange={(e) => setSelectedType(e.target.value)}
                            label="Tipo de Producto"
                        >
                            <MenuItem value="">Todos los tipos</MenuItem>
                            {types.map(type => (
                                <MenuItem key={type} value={type}>Tipo {type}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Box>

                {/* Products Grid */}
                <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 4 }}>
                {filteredProducts.map(product => (
                    <Card key={product.idProducto} sx={{
                        backgroundColor: '#ffccb8',
                        color: 'white',
                        borderRadius: 2,
                        transition: 'transform 0.3s ease',
                        '&:hover': {
                            transform: 'scale(1.05)',
                            boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)',
                        },
                    }}>
                        <CardContent>
                            {/* Título del Producto */}
                            <Typography variant="h6" sx={{ mb: 2, '&:hover': { color: '#fff' } }} noWrap>
                                {product.TituloProducto}
                            </Typography>

                            {/* Código Único */}
                            <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                                Código Único: {product.codigoUnico}
                            </Typography>

                            {/* Nombre de la Categoría y Año */}
                            <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                                <Typography variant="caption" sx={{
                                    backgroundColor: '#444',
                                    borderRadius: '16px',
                                    px: 2,
                                    py: 1,
                                    transition: 'background-color 0.3s ease',
                                    '&:hover': { backgroundColor: '#6b1414' },
                                }}>
                                    {product.categoriaNombre}
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                    Año: {product.ano}
                                </Typography>
                            </Box>

                            {/* Enlace para Visualización */}
                            {product.linkVisualizacion && (
                                <Box sx={{ mt: 2 }}>
                                    <a
                                        href={product.linkVisualizacion}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        style={{
                                            display: 'flex',
                                            alignItems: 'center',
                                            padding: '8px 16px',
                                            backgroundColor: '#3b82f6',
                                            color: 'white',
                                            borderRadius: '8px',
                                            textDecoration: 'none',
                                            fontSize: '14px',
                                            transition: 'background-color 0.3s ease',
                                        }}
                                        onMouseEnter={(e) => e.target.style.backgroundColor = '#2563eb'}
                                        onMouseLeave={(e) => e.target.style.backgroundColor = '#3b82f6'}
                                    >
                                        <Download sx={{ marginRight: '8px' }} />
                                        Descargar
                                    </a>
                                </Box>
                            )}
                        </CardContent>
                    </Card>
                ))}
            </Box>

                {/* Empty State */}
                {filteredProducts.length === 0 && (
                    <Box sx={{ textAlign: 'center', py: 6 }}>
                        <Typography variant="h6" color="textSecondary">No se encontraron productos que coincidan con tu búsqueda.</Typography>
                    </Box>
                )}
            </Box>
        </Box>
    );
};

export default Products;