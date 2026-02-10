% U+0035 DIGIT FIVE (5)
beginfig(53) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup loz_pen;

  % Top horizontal bar
  path topbar;
  topbar := (-(2/3)*x_radius-0.375*pen_height, y_radius)
            -- ((2/3)*x_radius, y_radius);
  draw topbar;

  % Vertical descent on the left (shorter to give bowl more room)
  pickup thin_pen;
  path stem;
  stem := (-(2/3)*x_radius, y_radius)
          -- (-(2/3)*x_radius, (1/6)*y_radius);
  draw stem;

  % Lower bowl — starts {down} to match stem direction, then curves
  % smoothly right and around to the lower-left terminal
  path lower_loop;
  lower_loop := (x_radius, (-1/2)*y_radius){down}
                .. tension 0.9
                .. (Ox, -y_radius){left}
                .. tension 0.9
                .. (-x_radius, Oy){up}
                .. tension 0.9
                .. (Ox, 0.75*y_radius){right}
                -- (x_radius, 0.75*y_radius)
                ;
  lower_loop := lower_loop scaled (2/3) shifted (0, -1/3*y_radius) reflectedabout ((0,0),(0,1));
  draw lower_loop;

endfig;
