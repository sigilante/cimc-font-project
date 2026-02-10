% U+E005 DESERET CAPITAL LETTER VARIANT SHORT A
beginfig(24581) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup loz_pen rotated 90;
  path bar;
  bar := (Ox, -y_radius - 0.325*pen_height) -- (Ox, y_radius);
  draw subpath(0, 0.75) of bar;

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

  pickup thin_pen;
  path outer_circle;
  outer_circle := (Ox, y_radius){left}
                  .. tension 0.9
                  .. (-x_radius, Oy){down}
                  .. tension 0.9
                  .. (Ox, -y_radius){right}
                  .. tension 0.9
                  .. (x_radius, Oy){up}
                  .. tension 0.9
                  .. cycle;

  draw outer_circle scaled (2/3) shifted (-2/3*x_radius, 1/3*y_radius);

endfig;
