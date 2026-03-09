# TriameseViT as feature extractor for FreeSurfer MRI processing
## Objectives

## Tools
### FreeSurfer
Using Apptainer(Singularity) to host Ubuntu20 image(docker).     

On dockerHub are available both the latest current stable(12/02/26) 7.4.1 and the 8_x (GPU enabled version)

#### 1. Pull the image(only once)
*Docker*
```bash
docker pull freesurfer/freesurfer:7.4.1
```

```bash
docker pull freesurfer/freesurfer:8.1.0
```

*Apptainer(Baldo cluster)*
```bash
apptainer pull freesurfer_7.4.1.sif docker://freesurfer/freesurfer:7.4.1
```

```bash
apptainer pull freesurfer_8.1.0.sif docker://freesurfer/freesurfer:8.1.0
```

#### 2. Licence File
To obtain the licence is necessary to visit https://surfer.nmr.mgh.harvard.edu/registration.html.

Compile the form and paste the `license.txt` file attached to confirmation email received

#### 3. Execute the image binding system directories

```bash
apptainer shell \
  --cleanenv \
  --bind /license.txt:/opt/freesurfer/license.txt \
  --bind /host-data:/data \
  --bind /FreeSurferOut \
  freesurfer_7.4.1.sif
```


```bash
apptainer shell \
--cleanenv \
--bind /license.txt:/opt/freesurfer/license.txt \
freesurfer_7.4.1.sif
```
- The `--cleanenv` is for omitting host ENV variables into the image
- The `--bind ~/license.txt:/opt/freesurfer/license.txt` is necessary for using FreeSurfer
- The `--bind /host-data:/data` is for mounting host data into FreeSurfer
- *(Optional)*The `/FreeSurferOut` is for mounting a host directory where storing the logs of FreeSurfer

#### Small guide
[Reference](https://www.youtube.com/watch?v=zeFPx0fMXRQ)

> [!Note]
> Free surfer takes volumetric data from MRI or fMRI scans and tries to reconstruct a **cortical surface** from those.
> The objective is extracting volumetric statistics of the parcelled cortical regions and sub-cortical structures

A digital cortical surface is represented as a **mesh**.

Important tasks made by FreeSurfer explicitly/implicitly:
- Cortex **Parcellation**, how cortex is labelled in regions
- *Sub-cortical* structures **Segmentation**, so the area division of all the *sub-cortical* structures

`recon-all` most important function. **It does all the FreeSurfer preprocessing**
There are 31 steps in these function, which are made to obtain the final inflated segmented surface.

This can be divided into 3 main blocks of ops.:
1. `autorecon-1` deals with the volume itself
2. `autorecon-2` which does smoothing and inflation
3. `autorecon-3` deals with registration it self used for the analysis


"rh" and "lh" stands for right emisphere and left emisphere.

There are many different output files, noticeable ones are:
- `aseg.mgz`: which is the result of the sub-cortex regions segmentation. (White matter, cortex....) **This might be an insert point for the ViT**
- ``: which is the result of computing the difference between the pial and the white matter boundary to compute the **gray matter thickness**
- `fsaverage`: is the average inflated surface derived sphere, used for intersubject comparison
- "annotation/.annot": are the files containing the parcellation step done after the sphere inflation(so after segmentation)
  1. .aparc.annot
  2. .a2009s.annot

**Parallelize the ops.(idk if i need this)**
```bash
ls *.nii | parallel --jobs 8 recon-all -s {.} -i {} -all 
```

ls *.nii or the other datatype you are computing


### Triamese-ViT
I'm removing all the useless models because I'm getting a lot of interferences with the dependencies

Flags for 
- `Training.py`:
  1. --train_folder
  1. --valid_folder
  1. --sorter 
  2. --excel_path

#### Spearman (differentiable) loss
>[!Warning]
> This loss is not used as described in the paper, it have been used instead the `mse`

The Spearman correlation coefficient tells how samples paired values are correlated in a monotonic but non-linear way.
It actually compare the **rank** for each sample from X to the rank from Y. The rank of a variable is an arbitrary ordering strategy of that variable, which means that exists an ordering relationship in the set (for example age, number of elements etc. etc.)

The ranking operations is non-differentiable, so a small model approximating the ranking function is the adopted solution from the authors.

> [!Warning]sorter
> If using the ranking aux_loss(default!) is necessary to have the "pretrained SoDeep sorter network weights"


There are 4 kinds of models used as "sorter" part for the Spearman loss:

#### FSL preprocessing


#### ComBat preprocessing
[original implementation](https://github.com/Jfortin1/ComBatHarmonization)
Harmonization done for scans coming from different machinery

```bash
python3 Training.py --train_folder data/IXI_test --valid_folder data/IXI_validate --excel_path ../IXI.xls
```

- `Prediction`:
  1. --train_folder
  2. --valid_folder
  3. --test_folder
  4. --excel_path
  

## References

- T1 IXI Dataset (581 healthy subjects)
  - web:  https://brain-development.org/ixi-dataset/
  - data: http://biomedic.doc.ic.ac.uk/brain-development/downloads/IXI/IXI-T1.tar
  - excel:http://biomedic.doc.ic.ac.uk/brain-development/downloads/IXI/IXI.xls 
