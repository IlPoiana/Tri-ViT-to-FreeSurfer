import argparse
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def plot_slices(nii_file, output_dir, slice_ranges=None):
    # Load the MRI data
    img = nib.load(nii_file)
    data = img.get_fdata()

    # Get the shape of the data
    n_slices_axial = data.shape[2]  # Number of axial slices
    n_slices_coronal = data.shape[1]  # Number of coronal slices
    n_slices_sagittal = data.shape[0]  # Number of sagittal slices
    
    if slice_ranges is None:
        # Set default slice ranges if not passed
        slice_ranges = {
            'axial': (0, n_slices_axial),
            'coronal': (0, n_slices_coronal),
            'sagittal': (0, n_slices_sagittal)
        }
    else:
        slice_ranges = {
            'axial': slice_ranges.get('axial', (0, n_slices_axial)),
            'coronal': slice_ranges.get('coronal', (0, n_slices_coronal)),
            'sagittal': slice_ranges.get('sagittal', (0, n_slices_sagittal))
        }

    # Ensure the slice ranges do not exceed the data dimensions
    for view in ['axial', 'coronal', 'sagittal']:
        start_slice, end_slice = slice_ranges[view]
        slice_ranges[view] = (
            max(0, start_slice),
            min(eval(f'n_slices_{view}'), end_slice)
        )

    # Plot and save each slice for each view
    for i in range(slice_ranges['axial'][0], slice_ranges['axial'][1]):
        plt.figure(figsize=(10, 8))
        plt.imshow(data[:, :, i], cmap='gray', vmin=data.min(), vmax=data.max())
        plt.title(f'Axial Slice {i}')
        plt.axis('off')
        plt.savefig(f'{output_dir}/axial/axial_slice_{i}.png')
        plt.close()

    for i in range(slice_ranges['coronal'][0], slice_ranges['coronal'][1]):
        plt.figure(figsize=(10, 8))
        plt.imshow(data[:, i, :], cmap='gray', vmin=data.min(), vmax=data.max())
        plt.title(f'Coronal Slice {i}')
        plt.axis('off')
        plt.savefig(f'{output_dir}/coronal/coronal_slice_{i}.png')
        plt.close()

    for i in range(slice_ranges['sagittal'][0], slice_ranges['sagittal'][1]):
        plt.figure(figsize=(10, 8))
        plt.imshow(data[i, :, :], cmap='gray', vmin=data.min(), vmax=data.max())
        plt.title(f'Sagittal Slice {i}')
        plt.axis('off')
        plt.savefig(f'{output_dir}/sagittal/sagittal_slice_{i}.png')
        plt.close()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Plot slices of a structural MRI scan in all three orientations.')
    parser.add_argument('nii_file', type=str, help='Path to the .nii.gz file')
    parser.add_argument('output_dir', type=str, help='Directory to save the output images')
    parser.add_argument('--slices', type=int, nargs=6, metavar=('axial_start', 'axial_end', 'coronal_start', 'coronal_end', 'sagittal_start', 'sagittal_end'), 
                        help='Range of slices to plot for each view (inclusive, zero-based)')
    args = parser.parse_args()
    
    # Prepare slice ranges
    slice_ranges = {}
    if args.slices:
        slice_ranges['axial'] = (args.slices[0], args.slices[1])
        slice_ranges['coronal'] = (args.slices[2], args.slices[3])
        slice_ranges['sagittal'] = (args.slices[4], args.slices[5])
    
    # Call the function to plot slices
    plot_slices(args.nii_file, args.output_dir, slice_ranges)
