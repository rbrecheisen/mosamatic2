import os
import shutil

DIR_INPUT = 'M:\\data\\zoe\\26-06-2026\\original\\Sternotomy_fixed_renamed'
NII_POSTFIX = '.seg.npy.nii.gz'
NII_EDIT_POSTFIX = '.seg.npyeditedTTD.nii.gz'


def main():

  # # Check matching DCM and NII file names
  # for f in os.listdir(DIR_INPUT):
  #   f_path = os.path.join(DIR_INPUT, f)
  #   if f.endswith('.dcm'):
  #     if not os.path.isfile(f'{f_path}{NII_EDIT_POSTFIX}'):
  #       print(f'{f}: edited not found')
  #     if not os.path.isfile(f'{f_path}{NII_POSTFIX}'):
  #       print(f'{f}: not found')

  # # Remove normal nii postfix files
  # for f in os.listdir(DIR_INPUT):
  #   f_path = os.path.join(DIR_INPUT, f)
  #   x = f'{f_path}{NII_POSTFIX}'
  #   if os.path.isfile(x):
  #     os.remove(x)

  # Rename edited nii files to normal
  for f in os.listdir(DIR_INPUT):
    f_path = os.path.join(DIR_INPUT, f)
    x = f'{f_path}{NII_EDIT_POSTFIX}'
    if os.path.isfile(x):
      y = f'{f_path}{NII_POSTFIX}'
      os.rename(x, y)



if __name__ == '__main__':
  main()