% U+0037 DIGIT SEVEN (7)
beginfig(55) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  % Top horizontal bar
  path topbar;
  topbar := (-(2/3)*x_radius, y_radius)
            -- ((2/3)*x_radius, y_radius);
  draw topbar;

  % Descending diagonal from right end of bar
  pickup thin_pen;
  path diagonal;
  diagonal := ((2/3)*x_radius, y_radius)
              -- (-(1/6)*x_radius, -y_radius);
  draw diagonal cutafter point 0.96 of diagonal;

  % Hanging serif at upper left (cf. Bee U+10411)
  pickup loz_pen rotated -90;
  path lserif;
  lserif := (-(2/3)*x_radius, y_radius)
            .. tension 0.9
            .. (-(2/3)*x_radius, (2/3)*y_radius);
  draw lserif;

  % Diagonal terminal serif
  path dserif;
  pair serif_dir;
  serif_dir := unitvector(direction 0 of diagonal);
  dserif := (point 0.97 of diagonal)
            -- (point 0.97 of diagonal) + 0.375*pen_height * serif_dir;
  rotatingdraw(dserif, 75, 90, 20, 0.6);

endfig;
