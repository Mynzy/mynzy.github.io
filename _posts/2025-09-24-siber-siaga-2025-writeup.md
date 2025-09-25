---
title: "Siber Siaga 2025 CTF Writeup"
date: 2025-09-24 12:00:00 +0800
categories: [CTF, Writeups, Online]
tags: [cybersecurity, ctf, siber-siaga, reverse-engineering, web-exploitation, pwn]
author: Mynz
---

# Siber Siaga 2025 CTF Writeup (Online)

My team, pulupuluultraman has managed to get 9th place and represent IIUM in Code Combat 2025 😆. This is my 1st CTF writeup and this writeup covers my solutions for 5 challenges from the Siber Siaga 2025 CTF competition. Special thanks to my team members, Jerit3787 & Rizzykun for carrying mee 🥳.

## Challenge 1: Spelling Bee

**Challenge Creator:** @penguincat  
**Connection:** `nc 5.223.49.127 57004`

### Description
Just spell the flag correctly then I will give it to you.

### Solution
Given the connection credentials, each attempt allows only 5 tries, but the 5th attempt never shows results, so effectively only 4 attempts are available.

![Spelling Bee Challenge](/assets/img/posts/SiberSiaga/SpellingBee.png )

Here is the result of my try and i combine it to get the flag

```
______5_____7___5____3______3________3_____7__
____R_______7___________4__________________7__
S_B__2_______1___________________1____________
_________0______________________________0___0_
___________________________b______tt_____t____
__________m___m__________n____________________
__________________l_____________l___l__p______
___________e___e_______c______________________
____________________f_____________tt_____t____
______________________________a___________a___
_I_E___{_____________________________________}
S_______s__________i__________________________
```

**Flag:** `SIBER25{s0me71me5_lif3_c4n_b3_a_l1ttl3_p0ta70}`

---

## Challenge 2: Entry to Meta City

**Challenge Creator:** @penguincat  
**URL:** `http://5.223.49.127:47001/`  
**Flag Format:** SIBER25{flag}

### Description
To gain entry to the prestige city, you will first need to prove your worth unless you are an admin.

### Solution
This challenge was quite straightforward. Just enter admin and you will get the flag

![Entry to Meta City Interface](/assets/img/posts/SiberSiaga/EntryToMetaCity.png)
_The login interface for Meta City_


![Flag Retrieved](/assets/img/posts/SiberSiaga/EntryToMetaCity2.png)
_Successfully retrieved flag after entering "admin" in the login page_

**Flag:** `SIBER25{w3lc0m3_70_7h3_c00l357_c17y}`

---

## Challenge 3: A Byte Tales

**Challenge Creator:** @penguincat  
**Connection:** `nc 5.223.49.127 57001`  
**Flag Format:** SIBER25{flag}

### Description
Choose your path and decide your own fate.

### Solution
Based on the source code given, you can see `flag.txt` which means the server will also have a file named `flag.txt` in it, now we just need to find ways to exploit it.

![A Byte Tales Source Code](/assets/img/posts/SiberSiaga/AByteTalesSourceCode.png)
![A Byte Tales Source Code](/assets/img/posts/SiberSiaga/AByteTalesSourceCode2.png)

In the code, you can find critical things which are `eval()` functions which can execute any command we put in the story as long as it is not in banned words.

For this im trying different combinations to get the flag

- `[open('flag.txt').read()]`
- `f"{open('flag.txt').read()}"`
- `repr(open('flag.txt').read())`

The successful payload that bypassed the filter was:

```python
__builtins__.__dict__['pr'+'int'](open('flag.txt').read())
```

![A Byte Tales Terminal Output](/assets/img/posts/SiberSiaga/AByteTalesTerminal.png)

This worked because it split the banned word "print" into parts and reconstructed it at runtime.

**Flag:** `SIBER25{St1ck_70_7h3_5toryl1n3!}`

---

## Challenge 4: Guess PWD

**Challenge Creator:** @y_1_16  
**Flag Format:** SIBER25{flag}

### Description
Only 4 digits, guess it!

### Solution
I guess I'm pushing my luck again today.
Given an apk file, so I'm using apktool (Sorry I'm just googling how to analyse apk files and apktool is one of the options) and in the command prompt i run this command to extract it.

```bash
apktool d app-debug.apk
```

After that, im opening vscode and just find SIBER25{

![Flag Search in VS Code](/assets/img/posts/SiberSiaga/GuessPWD.png)

Sorry for unintended solution 🙏

**Flag:** `SIBER25{y0u_cr4ck_l061n_w17h_wh47_w4y?}`

---

## Challenge 5: Deep on Adversarial

**Challenge Creator:** @penguincat  
**Flag Format:** SIBER25{flag}

### Description
Recently, our AI Tech Support behaved strangely. During investigation, we discovered two odd files on the culprit device are identical to a suspicious file from our server. We suspect something malicious is hidden inside the image itself, but we couldn't see it directly. Can you figure out how to uncover what's within the image that can only be seen by AI?

### Solution
I'm using Github Copilot with Claude Sonnet 4 as a model in this challenge. After a series of interrogation with the chatbot, im able to get the flag.

So, here's the code for solving the challenge. Below is one of the results from executing the program.

```python
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np
import os

def setup_model(model_path='model.pth'):
    """
    Load and setup the custom ResNet-18 model
    
    Args:
        model_path (str): Path to the model file
        
    Returns:
        torch.nn.Module: Loaded model ready for inference
    """
    print("🔧 Loading custom ResNet-18 model...")
    
    # Create ResNet-18 architecture
    model = models.resnet18()
    
    # Load the custom-trained weights
    state_dict = torch.load(model_path, map_location='cpu')
    model.load_state_dict(state_dict)
    model.eval()
    
    print("✅ Model loaded successfully!")
    return model

def setup_hooks(model):
    """
    Setup forward hooks to capture intermediate feature maps
    
    Args:
        model: PyTorch model
        
    Returns:
        dict: Dictionary to store captured feature maps
    """
    feature_maps = {}
    
    def hook_fn(name):
        def hook(module, input, output):
            feature_maps[name] = output.detach()
        return hook
    
    # Register hook on the first convolutional layer (most important for revealing hidden content)
    model.conv1.register_forward_hook(hook_fn('conv1'))
    
    print("🪝 Forward hooks registered on conv1 layer")
    return feature_maps

def preprocess_image(image_path='flag.png'):
    """
    Load and preprocess the image with minimal transformation
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        tuple: (PIL Image, torch tensor batch)
    """
    print(f"📷 Loading image: {image_path}")
    
    # Load the image
    image = Image.open(image_path)
    print(f"   Image size: {image.size}")
    print(f"   Image mode: {image.mode}")
    
    # Minimal preprocessing - preserve original information
    # Important: Don't use ImageNet normalization as it might destroy hidden content
    transform = transforms.Compose([
        transforms.ToTensor()  # Just convert to tensor, no resizing or normalization
    ])
    
    input_tensor = transform(image)
    input_batch = input_tensor.unsqueeze(0)  # Add batch dimension
    
    print(f"   Tensor shape: {input_batch.shape}")
    return image, input_batch

def feature_to_image(feature_map, normalize=True):
    """
    Convert a feature map tensor to a PIL Image
    
    Args:
        feature_map (torch.Tensor): 2D feature map
        normalize (bool): Whether to normalize to 0-255 range
        
    Returns:
        numpy.ndarray: Image array ready for PIL
    """
    if normalize:
        # Normalize to 0-1 range
        feature_map = (feature_map - feature_map.min()) / (feature_map.max() - feature_map.min())
    
    # Convert to 0-255 uint8 range
    feature_map = (feature_map * 255).clamp(0, 255).byte()
    return feature_map.numpy()

def extract_and_save_features(model, input_batch, feature_maps, output_dir='extracted_features'):
    """
    Run the model and extract feature maps, saving them as images
    
    Args:
        model: PyTorch model
        input_batch: Preprocessed image batch
        feature_maps: Dictionary to store feature maps
        output_dir: Directory to save feature images
    """
    print("🔍 Running model inference and extracting features...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Run inference
    with torch.no_grad():
        output = model(input_batch)
    
    # Extract conv1 features
    conv1_features = feature_maps['conv1'][0]  # Remove batch dimension
    print(f"   Conv1 features shape: {conv1_features.shape}")
    print(f"   Number of feature channels: {conv1_features.shape[0]}")
    
    # Save each feature channel as an image
    print("💾 Saving feature maps as images...")
    
    flag_candidates = []
    
    for i in range(conv1_features.shape[0]):  # Iterate through all channels
        # Convert feature map to image
        feature_img = feature_to_image(conv1_features[i])
        
        # Save as PNG
        output_path = os.path.join(output_dir, f'feature_conv1_ch{i:02d}.png')
        Image.fromarray(feature_img, mode='L').save(output_path)
        
        # Check if this channel might contain readable content
        # (Simple heuristic: check for high contrast areas that might be text)
        contrast_ratio = (feature_img.max() - feature_img.min()) / 255.0
        if contrast_ratio > 0.7:  # High contrast suggests potential text
            flag_candidates.append((i, contrast_ratio, output_path))
    
    print(f"✅ Saved {conv1_features.shape[0]} feature maps to '{output_dir}/'")
    
    # Report promising channels
    if flag_candidates:
        print("\n🎯 High-contrast channels (potential flag locations):")
        flag_candidates.sort(key=lambda x: x[1], reverse=True)  # Sort by contrast
        for channel, contrast, path in flag_candidates[:10]:  # Top 10
            print(f"   Channel {channel:2d}: {contrast:.3f} contrast -> {path}")
    
    return flag_candidates

def main():
    """
    Main function to extract the hidden flag
    """
    print("=" * 60)
    print("🚩 SIBER25 AI Steganography Challenge - Flag Extractor")
    print("=" * 60)
    
    try:
        # Step 1: Setup model
        model = setup_model()
        
        # Step 2: Setup hooks for feature extraction
        feature_maps = setup_hooks(model)
        
        # Step 3: Load and preprocess image
        original_image, input_batch = preprocess_image()
        
        # Step 4: Extract features and save them
        candidates = extract_and_save_features(model, input_batch, feature_maps)
        
        # Step 5: Provide guidance
        print("\n" + "=" * 60)
        print("🔍 NEXT STEPS:")
        print("=" * 60)
        print("1. Check the 'extracted_features/' directory")
        print("2. Look for files with readable text, especially:")
        
        if candidates:
            top_candidates = candidates[:5]  # Top 5 candidates
            for i, (channel, contrast, path) in enumerate(top_candidates, 1):
                print(f"   {i}. {os.path.basename(path)} (channel {channel})")
        else:
            print("   - feature_conv1_ch01.png")
            print("   - feature_conv1_ch05.png") 
            print("   - feature_conv1_ch06.png")
        
        print("\n3. The flag should be in format: SIBER25{...}")
        print("4. Channel 6 typically shows the clearest result!")
        
        print("\n✅ Feature extraction completed successfully!")
        print("🎯 Look for the clearest text in the generated images!")
        
    except FileNotFoundError as e:
        print(f"❌ Error: Required file not found - {e}")
        print("   Make sure 'flag.png' and 'model.pth' are in the current directory")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
```

<br>

![Adversarial Image](/assets/img/posts/SiberSiaga/DeepOnAdversarial.png "ICECTF{t00_ear1y_f0r_4_ctf}")

**Flag:** `SIBER25{l3arn1ng_m4ch1n3_l3arn1ng}`

---
## Scoreboard Siber Siaga 2025

![Scoreboard Siber Siaga 2025](/assets/img/posts/SiberSiaga/ScoreboardSiberSiaga.jpg)   