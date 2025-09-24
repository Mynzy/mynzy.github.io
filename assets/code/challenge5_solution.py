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