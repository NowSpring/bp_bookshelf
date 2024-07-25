import AppBar from '@mui/material/AppBar';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

const Header = () => {
  return (
    <div style={{ zIndex: 10, position: 'relative' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          bgcolor: "#ff1744",
          zIndex: (theme) => theme.zIndex.drawer + 1
        }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            ComicFaves
          </Typography>
        </Toolbar>
        
      </AppBar>
    </div>
  );
}

export default Header;
