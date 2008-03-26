! Python wrapper for the ephem module.
! F. Pierfederici (fpierfed@lsst.org)
subroutine ephemerides(typ, ndim, elements, t, h_mag, g_mag, &
  obscode, n, times, predictions, covar, norm)
  use ephem

  CHARACTER(LEN=3), intent(in) :: typ    
  ! elements type; known types are:
  !    'CAR' : cartesian positions and velocities 
  !    'EQU' : equinoctal elements
  !    'KEP' : classical keplerian elements, singular for
  !             0 eccentricity, 0 and 180 degrees inclination;
  !    'COM' : cometary elements, valid for ecc.ge.1 
  !    'ATT' : attributable plus r rdot
  !    'OPI' : Opik type elements not yet implemented
  INTEGER, intent(in) :: ndim  
  ! actual dimension of elements vector
  DOUBLE PRECISION, DIMENSION(6), intent(in) :: elements 
  ! elements vector DANGER: some of the coordinates may actually be angles...   
  DOUBLE PRECISION, DIMENSION(21), intent(in), optional :: covar 
  ! covariance matrix elements in diagonal form (only 21 elements).
  DOUBLE PRECISION, DIMENSION(21), intent(in), optional :: norm 
  ! normalization matrix elements in diagonal form (only 21 elements).
  DOUBLE PRECISION, intent(in) :: t  
  ! epoch time, MJD, TDT
  DOUBLE PRECISION, intent(in) :: h_mag, g_mag 
  ! Absolute magnitude H, opposition effect G
  ! INTEGER, intent(in) :: center 
  ! 0 for Sun, code for planet as in JPL ephemerides
  INTEGER, optional, intent(in) :: obscode 
  ! observatory code, for ATT type only
  INTEGER,INTENT(IN) :: n
  ! Number of elements in times.
  double precision, intent(in) :: times(n)
  ! List of MJDs to project the orbit to.
  double precision, intent(out) :: predictions(n, 7)
  ! List of [RA, Dec, T, ErrRa, ErrDec, PA] values.
  
  if(present(covar) .and. present(norm)) then
     call calc_ephem(typ, ndim, elements, t, h_mag, g_mag, &
          obscode, n, times, predictions, covar, norm)
  else
     call calc_ephem(typ, ndim, elements, t, h_mag, g_mag, obscode, &
          n, times, predictions)
  endif
end subroutine ephemerides

subroutine initialize()
  use ephem
  call init()
end subroutine initialize

subroutine time_convert(mjd, scale, out_mjd, out_scale)
  double precision, intent(in) :: mjd
  character*3, intent(in) :: scale, out_scale
  double precision, intent(out) :: out_mjd
  
  double precision sec1, sec2 
  integer imjd1, imjd2
  
  imjd1 = FLOOR(mjd)
  sec1 = (mjd - imjd1) * 86400.d0

  CALL cnvtim(imjd1, sec1, scale, &
       imjd2, sec2, out_scale)
  out_mjd = imjd2 + sec2 / 86400.d0
end subroutine
