
__all__ = ['freq', 'geometry', 'singlepoint', 'ts']


from qmflows.settings import Settings
import yaml

singlepoint = Settings(yaml.load("""
specific:
  adf:
     basis:
       type: SZ
     xc:
       __block_replace: true
       lda: ""
     numericalquality:
       normal
     scf:
       converge:
         1e-6
     iterations: 100
  ams:
     ams:
       Task: SinglePoint
  dftb:
    dftb:
      resourcesdir:
        "DFTB.org/3ob-3-1"
    task:
      runtype: SP

  cp2k:
    force_eval:
      dft:
        mgrid:
          cutoff: 400
          ngrids: 4
        print:
          mo:
            add_last: numeric
            each:
              qs_scf: 0
            eigenvalues: ""
            eigenvectors: ""
            filename: "./mo.data"
            ndigits: 36
            occupation_numbers: ""
        qs:
            method: gpw
        scf:
            eps_scf: 1e-06
            max_scf: 200
            scf_guess: restart

      subsys:
        cell:
          periodic: xyz
    global:
      print_level: low
      project: cp2k
      run_type: energy

  dirac:
    DIRAC: WAVEFUNCTION
    HAMILTONIAN: "LEVY-LEBLOND"
    WAVE FUNCTION: SCF

  gamess:
    basis:
      gbasis: sto
      ngauss: 3
    contrl:
      scftyp: rhf
      dfttyp: pbe

  orca:
    method:
        method: dft
        functional: lda
    basis:
        basis: sto_sz
""", Loader=yaml.FullLoader))

geometry = Settings(yaml.load("""
specific:
    adf:
      basis:
        type: SZ
      xc:
        __block_replace: true
        lda: ""
      numericalquality: good
      scf:
        converge: 1e-6
        iterations: 100
      geometry:
        optim: delocal
    ams:
       ams:
         Task: GeometryOptimization
         GeometryOptimization:
           MaxIterations: 500
    dftb:
        task:
          runtype: GO
        dftb:
          resourcesdir: "DFTB.org/3ob-3-1"
    dirac: Null

    cp2k:
      motion:
        geo_opt:
          type: minimization
          optimizer: bfgs
          max_iter: 500
      force_eval:
        dft:
          mgrid:
            cutoff: 400
            ngrids: 4
          qs:
            method: gpw
          scf:
            eps_scf: 1e-06
            max_scf: 200
            scf_guess: atomic
            OT:
              minimizer: DIIS
              N_DIIS: 7
              preconditioner: full_single_inverse
        subsys:
          cell:
            periodic: xyz
      global:
         print_level: low
         project: cp2k
         run_type: geometry_optimization
    orca:
        method:
            method: dft
            functional: lda
            runtyp: opt
        basis:
            basis: sto_sz
    gamess:
        basis:
          gbasis: n21
          ngauss: 3
        contrl:
          scftyp: rhf
          dfttyp: pbe
          runtyp: optimize
""", Loader=yaml.FullLoader))

# Transition state template
ts = Settings(yaml.load("""
specific:
  adf:
    basis:
      type: SZ
    xc:
      "__block_replace": true
      lda: ""
    numericalquality: good
    scf:
       converge: 1e-6
       iterations: 100
    geometry:
       transitionstate: "mode=1"
  dftb:
    task:
      runtype: TS
    dftb:
      resourcesdir: "DFTB.org/3ob-3-1"
  dirac: Null
  cp2k: Null
  orca:
    method:
      method: dft
      functional: lda
      runtyp: opt
    geom:
      ts_search: ef
    basis:
      basis: sto_sz
""",  Loader=yaml.FullLoader))

# Frequencies template
freq = Settings(yaml.load("""
specific:
  adf:
    analyticalfreq:
    basis:
      core: None
      type: DZP

    xc:
      "__block_replace": true
      lda: ""
    numericalquality: good

  ams:
    ams:
       Task: SinglePoint
       Properties:
          NormalModes: Yes

  dftb:
    task:
      runtype: Frequencies
    dftb:
      resourcesdir: "DFTB.org/3ob-3-1"
  dirac: Null
  cp2k : Null
  orca:
    method:
      method: dft
      functional: lda
    basis:
        basis: sto_sz
    main: freq
  gamess:
      basis:
        gbasis: n21
        ngauss: 3
      contrl:
        scftyp: rhf
        dfttyp: pbe
        runtyp: hessian
        nosym: 1
      force:
        method: seminum
""", Loader=yaml.FullLoader))
