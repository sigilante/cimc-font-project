% U+005D RIGHT SQUARE BRACKET (])
beginfig(93) ;
  pickup thin_pen;
  path bracket;
  bracket := (-(1/4)*x_radius, y_radius)
             -- ((1/4)*x_radius, y_radius)
             -- ((1/4)*x_radius, -y_radius)
             -- (-(1/4)*x_radius, -y_radius);
  draw bracket;
endfig;
