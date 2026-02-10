% U+005B LEFT SQUARE BRACKET ([)
beginfig(91) ;
  pickup thin_pen;
  path bracket;
  bracket := ((1/4)*x_radius, y_radius)
             -- (-(1/4)*x_radius, y_radius)
             -- (-(1/4)*x_radius, -y_radius)
             -- ((1/4)*x_radius, -y_radius);
  draw bracket;
endfig;
