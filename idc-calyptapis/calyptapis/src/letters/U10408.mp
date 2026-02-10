% U+10408 DESERET CAPITAL LETTER SHORT A (𐐈)
beginfig(1032) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup loz_pen rotated 90;
  path bar;
  bar := (Ox, -y_radius - 0.325*pen_height) -- (Ox, y_radius);
  draw bar;

  pickup loz_pen;
  path serif;
  serif := (-(1/3) * x_radius, y_radius)
          -- ((1/3) * x_radius, y_radius);
  draw serif;

  % Define the sweep path (with rotation/shift)
  path sweep_base, sweep;
  sweep_base := (-0.75*x_radius,-1.0*y_radius)
          .. tension 0.9
          .. (Ox,-1.0*y_radius-0.25*pen_height)
          .. tension 0.9
          .. (0.75*x_radius,-1.0*y_radius);

  sweep := sweep_base rotatedaround ((Ox,-y_radius),-15)
           shifted (Ox-0.75*cosd(-15)*x_radius,Oy-0.75*sind(-15)*y_radius);

  % Draw with rotating pen
  rotatingdraw(sweep, -15, 0, 20, 0.6);

endfig;
