% U+1041D DESERET CAPITAL LETTER ES (𐐝)
beginfig(1053);
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;
  path figure_eight;
  figure_eight := (Ox, y_radius){left}
                  .. tension 0.9
                  .. (-0.75x_radius, 0.5y_radius){down}
                  .. tension 0.9
                  .. (Ox, Oy){right}
                  .. tension 0.9
                  .. (0.75x_radius, -0.5y_radius){down}
                  .. tension 0.9
                  .. (Ox, -y_radius){left}
                  .. tension 0.9
                  .. (-0.75x_radius, -0.5y_radius){up}
                  .. tension 0.9
                  .. (Ox, Oy){right}
                  .. tension 0.9
                  .. (0.75x_radius, 0.5y_radius){up}
                  .. cycle
                  ;
  draw figure_eight;

  path loopl, loopr;
  loopr := (Ox,Oy){right}
           .. tension 0.9
           .. (1.25x_radius, -(1/2)*y_radius){down}
           ;
  draw loopr;
  loopl := (Ox,Oy){left}
           .. tension 0.9
           .. (-1.25x_radius, (1/2)*y_radius){up}
           ;
  draw loopl;

  pickup loz_pen rotated 90;
  path serif;
  serif := point 1 of loopl + (0,0.5*pen_height)
          -- point 1 of loopl;
  draw serif;
  pickup loz_pen rotated 90;
  serif := point 1 of loopr - (0, 0.5*pen_height)
          -- point 1 of loopr;
  draw serif;
endfig;
